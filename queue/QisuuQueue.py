#! /bin/python
#coding: utf-8

import Queue

class DuplexQueue(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DuplexQueue, cls).__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self):
        self.leftqueue = Queue.Queue()
        self.rightqueue = Queue.Queue()

    def leftpush(self, element):
        self.leftqueue.put(element)

    def leftpop(self):
        try:
            return self.leftqueue.get_nowait()
        except Queue.Empty:
            return None

    def leftempty(self):
        return self.leftqueue.empty()

    def leftsize(self):
        return self.leftqueue.qsize()

    def rightpush(self, element):
        self.rightqueue.put(element)

    def rightpop(self):
        try:
            return self.rightqueue.get_nowait()
        except Queue.Empty:
            return None

    def rightempty(self):
        return self.rightqueue.empty()

    def rightsize(self):
        return self.rightqueue.qsize()