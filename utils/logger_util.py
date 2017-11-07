# coding=UTF-8
import logging.handlers
import platform

LOG_DIR_WIN = "D:\\"
LOG_DIR_LINUX = "/home/zhangcc/logs/python_log/"


def get_logger(file_name):
    os_name = platform.platform()
    if ('Linux' in os_name):
        LOG_FILE_LINUX = LOG_DIR_LINUX + file_name
        handler = logging.handlers.RotatingFileHandler(LOG_FILE_LINUX, maxBytes=1024 * 1024, backupCount=5)
    else:
        LOG_FILE_WIN = LOG_DIR_WIN + file_name
        handler = logging.handlers.RotatingFileHandler(LOG_FILE_WIN, maxBytes=1024 * 1024, backupCount=5)

    fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
    formatter = logging.Formatter(fmt)  # 实例化formatter
    handler.setFormatter(formatter)
    logger = logging.getLogger('home-link')
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger
