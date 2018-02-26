#! /bin/python
# coding: utf-8

import logging
import time

class QisuuLog(object):
    
    def __init__(self, log_file='/tmp/qisuu_spider.log'):
        logging.basicConfig(filename=log_file, level=logging.DEBUG)

    def debug(self, message):
        debug_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        debug_info = '[DEBUG] {time} {message}'.format(
            time=debug_time,
            message=message,
        )
        logging.debug(debug_info)

    def info(self, message):
        info_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        info_info = '[INFO] {time} {message}'.format(
            time=info_time,
            message=message,
        )
        logging.info(info_info)

    def warn(self, message):
        warn_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        warn_info = '[WARN] {time} {message}'.format(
            time=warn_time,
            message=message,
        )
        logging.warn(warn_info)

    def error(self, message):
        error_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        error_info = '[ERROR] {time} {message}'.format(
            time=error_time,
            message=message,
        )
        logging.error(error_info)

    def critical(self, message):
        critical_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        critical_info = '[CRITICAL] {time} {message}'.format(
            time=critical_time,
            message=message,
        )
        logging.critical(critical_info)