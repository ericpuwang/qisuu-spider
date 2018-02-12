#! /bin/python
# coding: utf-8

from urllib2 import Request, urlopen
from threading import Thread
from logs.QisuuLog import QisuuLog
import threading
import time

_max_thread_num = 15

class Downloader(Thread):

    def __init__(self, url):
        self.url = url

        while threading.activeCount() > _max_thread_num:
            time.sleep(5)

        super(Downloader, self).__init__()

    def download(self):
        try:
            req = Request(self.url)
            res = urlopen(req)
            self.context = res.read()
        except Exception, e:
            self.context = ''
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            err_message = '{time} download {url} failure for {message}'.format(
                time=current_time,
                url=self.url,
                message=e.message,
            )
            QisuuLog(err_message)

    def run(self):
        self.download()
        if self.context:
            print 'download \033[32m {url} \033[0m succ'.format(url=self.url,)
        else:
            print 'download \033[31m {url} \033[0m fail'.format(url=self.url,)