# -*- coding: utf-8 -*-
# Author: dmhe
# Created on 2017-11-22
import os
import time
import threading
from collections import deque
import cPickle


__all__ = ['HEmpty', 'HQueue']


class HEmpty(Exception):
    pass


class HQueue:

    def __init__(self, path, maxsize=1000, clear=True):
        self.path = path
        if clear:
            self._clear_path()
        self.maxsize = maxsize
        self._init()
        self.mutex = threading.Lock()
        self.not_empty = threading.Condition(self.mutex)
        self.not_full = threading.Condition(self.mutex)
        self.all_tasks_done = threading.Condition(self.mutex)
        self.unfinished_tasks = 0

    def task_done(self):
        self.all_tasks_done.acquire()
        try:
            unfinished = self.unfinished_tasks - 1
            if unfinished <= 0:
                if unfinished < 0:
                    raise ValueError('task_done() called too many times')
                self.all_tasks_done.notify_all()
            self.unfinished_tasks = unfinished
        finally:
            self.all_tasks_done.release()

    def join(self):
        self.all_tasks_done.acquire()
        try:
            while self.unfinished_tasks:
                self.all_tasks_done.wait()
        finally:
            self.all_tasks_done.release()

    def qsize(self):
        self.mutex.acquire()
        n = self._qsize
        self.mutex.release()
        return n

    def empty(self):
        self.mutex.acquire()
        n = not self._qsize
        self.mutex.release()
        return n

    def put(self, item):
        self.not_full.acquire()
        try:
            self._put(item)
            self.unfinished_tasks += 1
            self.not_empty.notify()
        finally:
            self.not_full.release()

    def get(self, block=True, timeout=None):
        self.not_empty.acquire()
        try:
            if not block:
                if not self._qsize:
                    raise HEmpty
            elif timeout is None:
                while not self._qsize:
                    self.not_empty.wait()
            elif timeout < 0:
                raise ValueError("'timeout' must be a non-negative number")
            else:
                end_time = time.time() + timeout
                while not self._qsize:
                    remaining = end_time - time.time()
                    if remaining <= 0.0:
                        raise HEmpty
                    self.not_empty.wait(remaining)
            return self._get()
        finally:
            self.not_empty.release()

    def get_nowait(self):
        return self.get(False)

    def _init(self):
        self.queue = deque()
        self._qsize = 0
        self.tmp_queue = deque()
        self.file_queue = deque()
        self.file_num = 1
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def _put(self, item):
        if len(self.tmp_queue) == 0:
            if len(self.file_queue) == 0:
                if len(self.queue) < self.maxsize:
                    self.queue.append(item)
                else:
                    self.tmp_queue.append(item)
            else:
                self.tmp_queue.append(item)
        else:
            self.tmp_queue.append(item)
            if len(self.tmp_queue) == self.maxsize:
                self._write()
        self._qsize += 1

    def _write(self):
        file_name = 'q%d.cpk' % self.file_num
        with open(os.path.join(self.path, file_name), 'ab+') as f:
            cPickle.dump(self.tmp_queue, f, cPickle.HIGHEST_PROTOCOL)
            self.file_queue.append(file_name)
            self.tmp_queue.clear()
            self.file_num += 1

    def _get(self):
        if len(self.queue) == 0:
            if len(self.file_queue) > 0:
                self._read()
            else:
                self.queue, self.tmp_queue = self.tmp_queue, self.queue
        self._qsize -= 1
        return self.queue.popleft()

    def _read(self):
        file_name = self.file_queue.popleft()
        file_path = os.path.join(self.path, file_name)
        with open(file_path, 'rb') as f:
            self.queue = cPickle.load(f)
        os.remove(file_path)

    def _clear_path(self):
        if os.path.exists(self.path):
            for f in os.listdir(self.path):
                os.remove(os.path.join(self.path, f))
            os.rmdir(self.path)

    def __del__(self):
        self._clear_path()
