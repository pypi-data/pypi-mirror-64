# -*- coding: utf-8 -*-
# Author: dmhe
# Created on 2018-12-07
import pickle
import os
from collections import deque


__all__ = ['SimpleQueue', 'DiskQueue', 'PriorityQueue']


class SimpleQueue(object):

    def __init__(self):
        self.queue = deque()
        self.put = self.queue.append

    def get(self):
        queue = self.queue
        return queue.popleft() if queue else None

    def __len__(self):
        return len(self.queue)


class DiskQueue:

    def __init__(self, path, maxsize=1000, clear=True):
        self.path = path
        if clear:
            self._clear_path()
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.maxsize = maxsize
        self.queue = deque()
        self.tmp_queue = deque()
        self.file_queue = deque()
        self.file_num = 1
        self._qsize = 0

    def put(self, item):
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

    def get(self):
        if not self._qsize:
            return None
        if len(self.queue) == 0:
            if len(self.file_queue) > 0:
                self._read()
            else:
                self.queue, self.tmp_queue = self.tmp_queue, self.queue
        self._qsize -= 1
        return self.queue.popleft()

    def _write(self):
        file_name = 'q%d.cpk' % self.file_num
        with open(os.path.join(self.path, file_name), 'ab+') as f:
            pickle.dump(self.tmp_queue, f, pickle.HIGHEST_PROTOCOL)
            self.file_queue.append(file_name)
            self.tmp_queue.clear()
            self.file_num += 1

    def _read(self):
        file_name = self.file_queue.popleft()
        file_path = os.path.join(self.path, file_name)
        with open(file_path, 'rb') as f:
            self.queue = pickle.load(f)
        os.remove(file_path)

    def _clear_path(self):
        if os.path.exists(self.path):
            for f in os.listdir(self.path):
                os.remove(os.path.join(self.path, f))
            os.rmdir(self.path)

    def __len__(self):
        return self._qsize

    def __del__(self):
        self._clear_path()


class PriorityQueue(object):

    def __init__(self, queue_class, priorities, **kwargs):
        self.queues = {}
        self.priorities = sorted(priorities, reverse=True)
        for priority in self.priorities:
            if queue_class == DiskQueue:
                path = kwargs.get('path', None)
                if path:
                    path = os.path.join(path, str(priority))
                    self.queues[priority] = queue_class(path, kwargs.get('maxsize', 1000), kwargs.get('clear', True))
                else:
                    raise Exception('param path unset')

    def put(self, item, priority):
        if priority in self.queues:
            self.queues[priority].put(item)

    def get(self):
        for priority in self.priorities:
            if len(self.queues[priority]):
                return self.queues[priority].get()
        return None

    def __len__(self):
        return sum(len(x) for x in self.queues.values()) if self.queues else 0
