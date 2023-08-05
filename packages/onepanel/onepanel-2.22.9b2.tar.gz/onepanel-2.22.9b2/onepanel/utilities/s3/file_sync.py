from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

import concurrent.futures
import os.path
import datetime
import sys
import re
import logging

from onepanel.utilities.file import get_file_tree
from onepanel.utilities.time import UTC

from os.path import join
from threading import Lock
from onepanel.utilities.python_bridge import computer_cpu_count

FILE_SYNC_LOGGER = 'file_sync_logger'

class FileDifference:
    class State:
        MODIFIED = 'modified'
        NEW = 'new'
        DELETED = 'deleted'
        MOVED = 'moved'
    
    def __init__(self, source_path, destination_path, state, original_source_path=None, original_destination_path=None):
        """
        :param source_path: The source path of the file, assumed to be a filesystem path
        :type source_path: str
        :param destination_path: The destination path of the file, format is dependent on service used, like S3.
        :type destination_path: str
        :param state: The state of the file difference, NEW|MODIFIED|DELETED|MOVED. We assume that the difference
                      is from source to destination. E.g. source file is NEW relative to destination.
        :type state: str (one of the constants in FileDifference.State)
        :param original_source_path original path of file, if renaming or moving file.
        :type original_source_path str
        """

        if original_source_path is None:
            original_source_path = source_path

        if original_destination_path is None:
            original_destination_path = destination_path

        self.source_path = source_path
        self.original_source_path = original_source_path
        self.original_destination_path = original_destination_path
        self.destination_path = destination_path
        self.state = state

    def __str__(self):
        return "{{original_source: {}\nsource: {}\noriginal_destination: {}\ndestination: {}\nstate:{}}}"\
            .format(self.original_source_path, self.source_path,
                    self.original_destination_path, self.destination_path, self.state)


class FileEvent:
    START = 'start'
    FINISHED = 'finished'
    FAILED = 'failed'

    def __init__(self, state, file_difference, result=None):
        self.state = state
        self.file_difference = file_difference
        self.result = result


class FileSynchronizer:
    LOCAL = 0
    REMOTE = 1

    @staticmethod
    def filter_path(file_differences, path, prefix=None):
        if path[0] == '/':
            path = path[1:]

        result = {}
        for key, file_difference in file_differences.items():
            name = file_difference.destination_path
            if prefix is not None and prefix in name:
                name = name[len(prefix):]

            if name.startswith(path):
                result[file_difference.destination_path] = file_difference

        return result

    @staticmethod
    def filter(file_differences, regex, prefix=None):
        """
        :param file_differences: a map where name is a
        :param regex:
        :param prefix:
        :return:
        """

        result = {}
        pattern = re.compile(regex)
        for key, file_difference in file_differences.items():
            name = file_difference.destination_path
            if prefix is not None and prefix in name:
                name = name[len(prefix):]

            if pattern.search(name) is not None:
                result[name] = file_difference

        return result

    @staticmethod
    def local_file_stats(filepath):
        return {
            'last_modified': datetime.datetime.fromtimestamp(os.path.getmtime(filepath), UTC),
            'size': os.path.getsize(filepath)
        }
    
    @staticmethod
    def s3_file_stats(api_content):
        return {
            'last_modified': api_content['LastModified'],
            'size': api_content['Size']
        }

    @staticmethod
    def content_modification_difference_local(a, b):
        """
        Files are different if a has been modified after b, or, if equal,
        if the file sizes are different.
        :param a: local file
        :param b: remote file
        :return:
        """
        if a['last_modified'] > b['last_modified']:
            return True

        return a['size'] != b['size']

    @staticmethod
    def content_modification_difference_remote(a, b):
        """
        Files are different if a has been modified after b, or, if equal,
        if the file sizes are different.
        :param a: local file
        :param b: remote file
        :return:
        """
        return a['size'] != b['size']

    def __init__(self, filepath, s3_prefix, s3_wrapper, master=LOCAL, s3_full_path=None, ignore_file_states=None):
        """
        :param filepath:
        :type filepath str
        :param s3_prefix:
        :type s3_prefix str
        :param s3_wrapper:
        :type s3_wrapper onepanel.utilities.s3.wrapper.Wrapper
        :param master: Determines if the local files or the remote files are considered to be
                       the "master" and the opposite side should change its files to match it.
        :type master int one of the constants in FileSynchronizer
        :param s3_full_path: The full s3 path to get files from. Used to select subfolders.
                In this case s3_prefix is the "root" of the files, so the names will be relative to that.
        :param ignore_file_states: A list of file states to ignore. These will not be synchronized, etc.
        :param include_glob: A glob pattern of files to include. Files not matching this pattern will not be included.
        :type str
        """
        self.filepath = filepath
        self.s3_prefix = s3_prefix
        self.master = master
        self.s3_wrapper = s3_wrapper
        self.s3_full_path = s3_full_path

        if ignore_file_states is None:
            ignore_file_states = []

        self.ignore_file_states = ignore_file_states
        self.running = True

    def find_difference(self, comparator=None):
        """ Finds the differences in files between the file_path and s3_prefix using
        the provided master.
        :return: a map of the file differences. Key is file path locally, value is a FileDifference
        :type {}
        """

        if comparator is None and self.master == FileSynchronizer.LOCAL:
            comparator = FileSynchronizer.content_modification_difference_local
        elif comparator is None and self.master == FileSynchronizer.REMOTE:
            comparator = FileSynchronizer.content_modification_difference_remote

        if self.master == FileSynchronizer.LOCAL:
            return self._find_difference_local(comparator)
        else:
            return self._find_difference_remote(comparator)

    def _find_difference_local(self, comparator):
        differences = {}

        s3_keys = self.s3_wrapper.list_files(self.s3_prefix)

        files = get_file_tree(self.filepath)

        # +1 to remove filepath separator
        local_filepath_length = len(self.filepath) + 1

        for filepath in files:
            path = join(self.s3_prefix, filepath[local_filepath_length:])
            path = path.replace('\\', '/')
            if path in s3_keys:
                modified = comparator(FileSynchronizer.local_file_stats(filepath),
                                      FileSynchronizer.s3_file_stats(s3_keys[path]))

                if modified:
                    differences[filepath] = FileDifference(filepath, path, FileDifference.State.MODIFIED)

                del s3_keys[path]
            else:
                differences[filepath] = FileDifference(filepath, path, FileDifference.State.NEW)

        s3_prefix_length = len(self.s3_prefix)
        for remote_path in s3_keys.keys():
            local_path = join(self.filepath, remote_path[s3_prefix_length:])
            differences[local_path] = FileDifference(local_path, remote_path, FileDifference.State.DELETED)

        to_remove = []
        for file_path, value in differences.items():
            if value.state in self.ignore_file_states:
                to_remove.append(file_path)

        for file_path in to_remove:
            del differences[file_path]

        return differences

    def _find_difference_remote(self, comparator):
        differences = {}

        file_path = self.s3_prefix
        if self.s3_full_path is not None:
            file_path = self.s3_full_path

        s3_keys = self.s3_wrapper.list_files(file_path)
        files = get_file_tree(self.filepath)

        s3_prefix_length = len(self.s3_prefix)

        for key, value in s3_keys.items():
            path = join(self.filepath, key[s3_prefix_length:])

            if sys.platform == "win32":
                path = path.replace("/", "\\")

            if path in files:
                modified = comparator(FileSynchronizer.local_file_stats(path),
                                      FileSynchronizer.s3_file_stats(value))

                if modified:
                    differences[path] = FileDifference(path, key, FileDifference.State.MODIFIED)

                files.remove(path)
            else:
                differences[path] = FileDifference(path, key, FileDifference.State.NEW)

        for local_path in files:
            remote_path = join(self.s3_prefix, local_path[(len(self.filepath) + 1):])
            differences[local_path] = FileDifference(local_path, remote_path, FileDifference.State.DELETED)

        to_remove = []
        for file_path, value in differences.items():
            if value.state in self.ignore_file_states:
                to_remove.append(file_path)

        for file_path in to_remove:
            del differences[file_path]

        return differences

    def synchronize(self, file_differences, hooks=None):
        for difference in file_differences:
            self.synchronize_single(difference, hooks)

    def synchronize_single(self, file_difference, hooks=None, max_threads=None):
        """
        Synchronizes the file between local and remote. Uses the master specified in the constructor.

        :param file_difference:
        :type file_difference FileDifference
        :param hooks
        :param max_threads the maximum number of threads to use for the network operation.
        :return: result of the sync
        """

        if file_difference.state in self.ignore_file_states:
            return

        self.call_hooks(hooks, FileEvent(FileEvent.START, file_difference))
        try:
            if self.master == FileSynchronizer.LOCAL:
                result = self._synchronize_local_master(file_difference, max_threads=max_threads)
            else:
                result = self._synchronize_remote_master(file_difference, max_threads=max_threads)

            self.call_hooks(hooks, FileEvent(FileEvent.FINISHED, file_difference, result))
        except BaseException as exception:
            self.call_hooks(hooks, FileEvent(FileEvent.FAILED, file_difference, exception))

    def _synchronize_local_master(self, file_difference, max_threads=None):
        if file_difference.state == FileDifference.State.NEW:
            return self.s3_wrapper.upload_file(file_difference.source_path, file_difference.destination_path,
                                               max_threads=max_threads)
        elif file_difference.state == FileDifference.State.MODIFIED:
            return self.s3_wrapper.upload_file(file_difference.source_path, file_difference.destination_path,
                                               max_threads=max_threads)
        elif file_difference.state == FileDifference.State.DELETED:
            return self.s3_wrapper.delete_file(file_difference.destination_path)
        elif file_difference.state == FileDifference.State.MOVED:
            return self.s3_wrapper.move_file(file_difference.original_destination_path, file_difference.destination_path)

    def _synchronize_remote_master(self, file_difference, max_threads=None):
        if file_difference.state == FileDifference.State.NEW:
            return self.s3_wrapper.download_file(file_difference.source_path, file_difference.destination_path,
                                                 max_threads=max_threads)
        elif file_difference.state == FileDifference.State.MODIFIED:
            os.remove(file_difference.source_path)
            return self.s3_wrapper.download_file(file_difference.source_path, file_difference.destination_path,
                                                 max_threads=max_threads)
        elif file_difference.state == FileDifference.State.DELETED:
            os.remove(file_difference.source_path)
            return True
        elif file_difference.state == FileDifference.State.MOVED:
            raise NotImplementedError('Unable to tell if a file was moved on s3')

    def shutdown(self):
        self.running = False

    def call_hooks(self, hooks, file_event):
        if not self.running:
            return

        if hooks is None:
            return

        for hook in hooks:
            hook(file_event)

    @staticmethod
    def print_status(cwd_length, master=LOCAL):
        """Returns a function that takes in a file_difference and prints the action on the input file
        Uses the current working directory length to print relative file names.
        """

        def print_status_internal_local(file_event):
            """
             :param file_event:
             :type file_event FileEvent
             :return:
             """
            if file_event.state == FileEvent.START:
                return

            file_difference = file_event.file_difference

            local_path = file_difference.source_path[cwd_length:]

            if file_difference.state == FileDifference.State.MOVED:
                local_source_path = file_difference.original_source_path[cwd_length:]

                if file_event.state == FileEvent.FINISHED:
                    print('move {} to {}'.format(local_source_path, local_path))
                elif file_event.state == FileEvent.FAILED:
                    print('(FAILED) move {} to {}'.format(local_source_path, local_path))
                else:
                    print('move {} to {}'.format(local_source_path, local_path))

                return

            action = 'upload'

            if file_difference.state == FileDifference.State.DELETED:
                action = 'delete'

            if file_difference.state == FileDifference.State.MODIFIED:
                action = 'upload modified'

            if file_event.state == FileEvent.FAILED:
                action = '(FAILED) {} - {}'.format(action, file_event.result)

            print('{}: {}'.format(action, local_path))

        def print_status_internal_remote(file_event):
            """

            :param file_event:
            :type file_event FileEvent
            :return:
            """
            if file_event.state == FileEvent.START:
                return

            file_difference = file_event.file_difference

            # Pick out the version of the remote folder.
            # Want to display account_uid / datasets / dataset_uid / path / to / file.txt
            local_path = file_difference.original_destination_path
            parts = local_path.split('/', 4)
            del parts[3]
            local_path = "/".join(parts)

            if file_difference.state == FileDifference.State.MOVED:
                local_source_path = file_difference.original_source_path[cwd_length:]
                print('move {} to {}'.format(local_source_path, local_path))
                return

            action = 'download'

            if file_difference.state == FileDifference.State.DELETED:
                action = 'delete'

            if file_difference.state == FileDifference.State.MODIFIED:
                action = 'download modified'

            if file_event.state == FileEvent.FAILED:
                action = '(FAILED) {} - {}'.format(action, file_event.result)

            print('{}: {}'.format(action, '/' + local_path))

        if master == FileSynchronizer.LOCAL:
            return print_status_internal_local

        return print_status_internal_remote


class SynchronizingFile:
    def __init__(self, file_difference, max_attempts=5):
        self.file_difference = file_difference
        self.attempts = 0
        self._max_attempts = max_attempts

    def should_retry(self):
        return self.attempts < self._max_attempts

    def retry(self):
        self.attempts += 1


class ThreadedFileSynchronizer:
    def __init__(self, synchronizer, hooks=None, logging_verbose=True):
        self.synchronizer = synchronizer
        self.executor = concurrent.futures.ThreadPoolExecutor()
        self.backlog = {}
        self.active_items = {}
        self.hooks = hooks
        self.lock = Lock()
        self.running = True
        self.max_threads = (computer_cpu_count() or 1) * 10

        self.logger = logging.getLogger(FILE_SYNC_LOGGER)
        if logging_verbose:
            self.logger.setLevel(logging.INFO)
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

    def find_difference(self, comparator=None):
        return self.synchronizer.find_difference(comparator)

    def synchronize(self, file_differences):
        for difference in file_differences:
            self.synchronize_single(difference)

    def synchronize_single(self, file_difference):
        """
        :param file_difference:
        :type file_difference FileDifference
        :return:
        """
        with self.lock:
            # Ensure operations on the same source file are done in order they come in
            for current_task in self.active_items.values():
                if current_task.file_difference.original_source_path == file_difference.original_source_path:
                    self._add_to_backlog(file_difference)
                    return

        self._execute_item(file_difference)

    def _execute_item(self, file_difference):
        if not self.running:
            return

        task = self.executor.submit(self.synchronizer.synchronize_single, file_difference, self.hooks, self.max_threads)

        with self.lock:
            self.active_items[task] = SynchronizingFile(file_difference)

        task.add_done_callback(self._on_task_completed)

    def shutdown(self, wait=True):
        if not wait:
            self.synchronizer.shutdown()

        self.running = False
        self.backlog = {}
        self.executor.shutdown(wait)

    def _on_task_completed(self, arg):
        """
        :param arg
        :type arg concurrent.futures.Future
        """

        with self.lock:
            syncing_file = self.active_items[arg]

            if arg.exception() is not None and syncing_file.should_retry():
                self.logger.info("Retrying {}".format(syncing_file.file_difference.source_path))
                syncing_file.retry()
                self._execute_item(syncing_file.file_difference)
                return

            del self.active_items[arg]

        backlog = self._get_backlog(syncing_file.file_difference)
        if backlog is not None:
            self._execute_item(backlog)

    def _add_to_backlog(self, file_difference):
        key = file_difference.original_source_path
        if key in self.backlog:
            self.backlog[key].append(file_difference)
            return

        self.backlog[key] = [file_difference]

    def _get_backlog(self, file_difference):
        key = file_difference.original_source_path
        if key not in self.backlog:
            return None

        todo = self.backlog[key]
        if len(todo) == 0:
            return None

        return todo.pop()
