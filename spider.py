#! /bin/python
# coding: utf-8

'''
relative_url
/soft/sort[01-10]/index_[1-?].html
'''

from download.QisuuThread import Downloader
from parser.QisuuBs4 import Parser
from queue.QisuuQueue import DuplexQueue
import threading
import time
import sys

_duplex_queue = DuplexQueue()

seed_url = 'http://www.80txt.com/sort{number}/1.html'
for i in range(1, 26):
    url = seed_url.format(number=i)
    _duplex_queue.rightpush(url)

_max_down_thread_num = 5
_max_parse_thread_num = 5

def download():
    down_thread = []
    for i in range(_max_down_thread_num):
        down_thread.append(Downloader())

    for thread in down_thread:
        thread.start()

    while True:
        for thread in down_thread:
            if not thread.isAlive():
                thread = Downloader()
                thread.start()

def parser():
    parse_thraed = []
    while _duplex_queue.leftempty():
        time.sleep(1)

    for i in range(_max_parse_thread_num):
        parse_thraed.append(Parser())

    for thread in parse_thraed:
        thread.start()

    while True:
        for thread in parse_thraed:
            if not thread.isAlive():
                thread = Parser()
                thread.start()

if __name__ == '__main__':
    down = threading.Thread(target=download)
    down.start()

    parse = threading.Thread(target=parser)
    parse.start()

    #if _duplex_queue.leftempty() and _duplex_queue.rightempty():
    #    sys.exit('qisuu spider finish')