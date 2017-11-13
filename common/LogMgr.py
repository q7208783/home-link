#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
import logging, logging.handlers
import platform

LOG_DIR_WIN = "D:\\"
LOG_DIR_LINUX = "/home/zhangcc/logs/python_log/"

class LogMgr:
    def __init__(self, logpath):
        self.LOG = logging.getLogger(logpath)
        os_name = platform.platform()
        if ('Linux' in os_name):
            path = LOG_DIR_LINUX + logpath
        else:
            path = LOG_DIR_WIN + logpath
        loghdlr1 = logging.handlers.RotatingFileHandler(path, "a", 0, 1)
        fmt1 = logging.Formatter("%(asctime)s %(threadName)-10s %(message)s", "%Y-%m-%d %H:%M:%S")
        loghdlr1.setFormatter(fmt1)
        self.LOG.addHandler(loghdlr1)
        self.LOG.setLevel(logging.DEBUG)

    def error(self, msg):
        if self.LOG is not None:
            self.LOG.error(msg)

    def info(self, msg):
        if self.LOG is not None:
            self.LOG.info(msg)

    def debug(self, msg):
        if self.LOG is not None:
            self.LOG.debug(msg)

    def mark(self, msg):
        if self.MARK is not None:
            self.MARK.info(msg)


def main():
    global log_mgr
    log_mgr = LogMgr("mylog")
    log_mgr.error('[mylog]This is error log')
    log_mgr.info('[mylog]This is info log')
    log_mgr.debug('[mylog]This is debug log')


if __name__ == "__main__":
    main()
