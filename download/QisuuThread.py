#! /bin/python
# coding: utf-8

from urllib2 import Request, urlopen
from threading import Thread
from logs.QisuuLog import QisuuLog
from queue.QisuuQueue import DuplexQueue
import threading
import time

_max_thread_num = 15
_duplex_queue = DuplexQueue()


class Downloader(Thread):

    def __init__(self, url):
        self.url = url
        self.log = QisuuLog()

        while threading.activeCount() > _max_thread_num:
            time.sleep(5)

        super(Downloader, self).__init__()

    def download(self):
        try:
            req = Request(self.url)
            res = urlopen(req)
            self.context = res.read()
            message = 'download {url} succ'.format(url=self.url,)
            self.log.debug(message)
        except Exception, e:
            self.context = ''
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            err_message = 'download {url} failure for {message}'.format(
                url=self.url,
                message=e.message,
            )
            self.log.error(err_message)

    def run(self):
        self.download()
        if self.context:
            _duplex_queue.leftpush({'url': self.url, 'content': self.context})
            print 'download \033[32m {url} \033[0m succ'.format(url=self.url,)
        else:
            print 'download \033[31m {url} \033[0m fail'.format(url=self.url,)