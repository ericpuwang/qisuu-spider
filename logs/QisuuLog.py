#! /bin/python
# coding: utf-8

import logging
import time

class QisuuLog(object):
    
    def __init__(self, log_file='/tmp/qisuu_spider.log'):
        logging.basicConfig(filename=log_file, level=logging.DEBUG)

    def _now(self):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return current_time

    def debug(self, message):
        debug_info = '[DEBUG] {time} {message}'.format(
            time=self._now(),
            message=message,
        )
        logging.debug(debug_info)

    def info(self, message):
        info_info = '[INFO] {time} {message}'.format(
            time=self._now(),
            message=message,
        )
        logging.info(info_info)

    def warn(self, message):
        warn_info = '[WARN] {time} {message}'.format(
            time=self._now(),
            message=message,
        )
        logging.warn(warn_info)

    def error(self, message):
        error_info = '[ERROR] {time} {message}'.format(
            time=self._now(),
            message=message,
        )
        logging.error(error_info)

    def critical(self, message):
        critical_info = '[CRITICAL] {time} {message}'.format(
            time=self._now(),
            message=message,
        )
        logging.critical(critical_info)