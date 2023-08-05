import os
import sys
import logging

import click

from onepanel.commands.base import APIViewController
from onepanel.commands import jobs
from onepanel.commands.datasets import DatasetViewController, DatasetIdentifier, _datasets_push
from onepanel.commands.jobs import jobs_download_output, JobViewController
from onepanel.commands.login import login_required
from onepanel.commands.projects import projects_clone
from onepanel.utilities.timer import Timer, WaitTimer
from onepanel.utilities.process import run_in_background

COMMON_LOGGER = 'common_logger'


def get_entity_type(path):
    dirs = path.split('/')

    entity_type = None
    if len(dirs) == 3:
        account_uid, dir, uid = dirs
        if dir == 'projects':
            entity_type = 'project'
        elif dir == 'datasets':
            entity_type = 'dataset'
    elif len(dirs) == 5:
        account_uid, parent, project_uid, dir, uid = dirs
        if parent == 'projects' and dir == 'jobs':
            entity_type = 'job'

    if len(dirs) > 2 and dirs[1] == 'datasets':
        entity_type = 'dataset'

    return entity_type


@click.command('clone', help='Clone a remote project', hidden=True)
@click.argument('path', type=click.Path())
@click.argument('directory', type=click.Path(), required=False)
@click.option(
    '-q', '--quiet',
    is_flag=True,
    help='Minimize chatter from executed commands.'
)
@click.pass_context
@login_required
def clone(ctx, path, directory,quiet):
    entity_type = get_entity_type(path)
    if entity_type == 'project':
        projects_clone(ctx, path, directory)
    elif entity_type == 'dataset':
        vc = DatasetViewController(ctx.obj['connection'])
        identifier = DatasetIdentifier(path)

        if directory is None or directory == '.':
            directory = os.getcwd()
        else:
            directory = os.path.join(os.getcwd(), directory)

        vc.clone(identifier, directory, quiet)
    else:
        click.echo('Invalid project or dataset path.')


@click.command('download', help='Download a dataset or job output')
@click.argument('path', type=click.Path())
@click.argument('directory', type=click.Path(), required=False)
@click.option(
    '--delete',
    type=bool,
    is_flag=True,
    default=False,
    help='Deletes files locally that are not in the dataset'
)
@click.option(
    '--archive',
    type=bool,
    is_flag=True,
    default=False,
    help='Download the job output as a compressed file. Applies to Jobs only.'
)
@click.option(
    '-q', '--quiet',
    is_flag=True,
    help='Minimize chatter from executed commands.'
)
@click.option(
    '-b', '--background',
    is_flag=True,
    help='Run the download in the background. Will work even if SSH session is terminated.'
)
@click.option(
    '-v', '--version',
    type=str,
    help='The version of the dataset. If none is provided, latest is used.')
@click.option(
    '--include',
    type=str,
    help='Only include files matching this regex pattern.'
)
@click.pass_context
@login_required
def download(ctx, path, directory, archive, quiet, background, version, delete, include):
    entity_type = get_entity_type(path)
    if entity_type == 'dataset':
        dataset_identifier = DatasetIdentifier(path, version)
        vc = DatasetViewController(ctx.obj['connection'])

        if directory is None or directory == '.':
            directory = os.getcwd()
        else:
            directory = os.path.join(os.getcwd(), directory)

        if background:
            cmd_list = sys.argv
            cmd_list.remove('-b')
            run_in_background(cmd_list)
            click.echo("Starting download in the background.")
        else:
            print('Downloading...')
            try:
                vc.download(dataset_identifier, directory, quiet, delete, include)
            except APIViewController.NotFoundException:
                click.echo('Either the dataset does not exist or you do not have access to it')
            except APIViewController.UnauthorizedException:
                click.echo('Either the dataset does not exist or you do not have access to it')

    elif entity_type == 'job':
        jobs_download_output(ctx, path, directory, archive)
    else:
        click.echo('Invalid path.')


@click.command('push', help='Push changes to onepanel', hidden=True)
@click.option(
    '-p', 'entity_path',
    type=str,
    help='Specifies an entity to push to. Something like account_uid/entity_type/entity_uid'
)
@click.option(
    '-m', '--message',
    type=str,
    default=None,
    help='Add a message to this push.'
)
@click.option(
    '-n', '--name',
    type=str,
    default=None,
    help='Add a name to this push.'
)
@click.option(
    '-u', '--update-version',
    is_flag=True,
    default=False,
    help='Create a new version and push.'
)
@click.option(
    '-q', '--quiet',
    is_flag=True,
    help='Minimize chatter from executed commands.'
)
@click.option(
    '-b', '--background',
    is_flag=True,
    help='Run in background. Will work even if SSH session is terminated.'
)
@click.option(
    '-w', '--watch',
    is_flag=True,
    help='Watches and pushes any changes to local files.'
)
@click.option(
    '-y', '--yes',
    is_flag=True,
    default=False,
    help='Automatic yes to prompts'
)
@click.option(
    '--in-background',
    is_flag=True,
    default=False,
    hidden=True
)
@click.pass_context
@login_required
def push(ctx, entity_path,  message, name, quiet, background, update_version, watch, yes, in_background):
    # Are we uploading job output? A project? Or Dataset?
    if os.path.isfile(JobViewController.JOB_OUTPUT_FILE):
        jobs.upload_directory_raw(ctx, source_directory=os.curdir, delete=True)
    elif os.path.isfile(DatasetViewController.DATASET_FILE) or entity_path is not None:
        _datasets_push(ctx, entity_path, message, name, update_version, quiet, background, watch, in_background)
    else:
        click.echo("Cannot determine if you are trying to push job output, dataset files, or project files. "
                   "Are you in the right directory?")


@click.command('timer-sync-output', help='Syncs job output and logs repeated on a timer', hidden=True)
@click.option('-j', '--job_uid', type=str, help='The job uid')
@click.option('-p', '--project_uid', type=str, help='The uid of the project the job is for')
@click.option('-a', '--project_account_uid', type=str, help='The uid of the account that owns the project the job is in')
@click.option('-d', '--delay', type=str, help='What interval the timer sends a request')
@click.option('-s', '--path', type=str, help='Path to sync files from')
@click.option('-r', '--destination', type=str, help='Path to sync files to')
@click.option('-x', '--delete', type=bool, is_flag=True,  help='Path to sync files to')
@click.option('-v', '--verbose', type=bool, is_flag=True, help='If command should log what it is doing')
@click.pass_context
@login_required
def timer_sync_output(ctx, job_uid, project_uid, project_account_uid, path, destination, delay, delete, verbose):
    if verbose is None:
        verbose = False

    if verbose:
        logger = logging.getLogger(COMMON_LOGGER)
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    if delay is None:
        delay = 5.0
    else:
        if verbose:
            logger.info('Delay passed in: ' + delay + ' type: ' + str(type(delay)))

        delay = float(delay)

    def onepanel_push_wrapper():
        if not os.path.exists(path):
            logging.getLogger(COMMON_LOGGER).info('Waiting until path {} exists'.format(path))
            # Wait until path exists
            return

        logging.getLogger(COMMON_LOGGER).info('Sync: {}/{}/{}: {} -> {}'.
                                              format(project_account_uid, project_uid, job_uid, path, destination))
        jobs.upload_directory_raw(ctx, project_account_uid, project_uid, job_uid, source_directory=path, destination_directory=destination, delete=delete)

    timer = WaitTimer(delay, onepanel_push_wrapper)
    timer.start()
    timer.join()
