# -*- coding:utf-8 -*-
""" Provide log related functions. You need to Initialize the logger and use the logger to make logs.

Example:

>>> logger = Initialize()

Use logger.level(\*msg) to log like:

>>> logger.error("Pickle data writing Failed.")

>>> logger.info("Pickle data of ", foo, " written successfully.")

The log will be stored into LogFile.log by default.
"""

__author__ = "Wang Hewen"

import sys
import logging

logging.currentframe = lambda: sys._getframe(5)
class Logger(logging.Logger):
    def debug(self, *args, **kwargs):
        super().log("".join([str(arg) for arg in args]), **kwargs)

    def info(self, *args, **kwargs):
        super().info("".join([str(arg) for arg in args]), **kwargs)

    def warning(self, *args, **kwargs):
        super().warning("".join([str(arg) for arg in args]), **kwargs)

    def warn(self, *args, **kwargs):
        super().warn("".join([str(arg) for arg in args]), **kwargs)

    def error(self, *args, **kwargs):
        super().error("".join([str(arg) for arg in args]), **kwargs)

    def exception(self, *args, exc_info=True, **kwargs):
        super().exception("".join([str(arg) for arg in args]), exc_info = exc_info, **kwargs)

    def critical(self, *args, **kwargs):
        super().critical("".join([str(arg) for arg in args]), **kwargs)

    def log(self, level, *args, **kwargs):
        super().log(level, "".join([str(arg) for arg in args]), **kwargs)

    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False):
        super()._log(level, msg, args, exc_info=None, extra=None, stack_info=False)


def Initialize(FileName = "LogFile.log", LogLevel = "INFO", WriteToStream = False):
    '''
Initialize loggers for logging. A logger will be returned.

:param String FileName: Path of the log file
:param String LogLevel: LogLevel of the logger, which can be "DEBUG", "INFO", "ERROR"
:param Boolean WriteToStream: Whether to write to stdout
:return: logger: The logger used for logging
:rtype: logging.loggger
    '''
    if LogLevel not in ["DEBUG", "INFO", "ERROR"]:
        raise ValueError("LogLevel is not correctly set.")
    logging.Logger.manager.setLoggerClass(Logger)
    logger = logging.getLogger(__name__) #__name__ == CommonModules.Log
    handlers = logger.handlers[:]
    for handler in handlers:
        handler.close()
        logger.removeHandler(handler)
    fileHandler = logging.FileHandler(FileName)
    fileHandler.setFormatter(logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s', datefmt = '%Y/%m/%d %H:%M:%S'))
    if LogLevel == "DEBUG":
        streamHandler = logging.StreamHandler(stream = sys.stdout)
        streamHandler.setLevel(logging.DEBUG)
        fileHandler.setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
    if LogLevel == "INFO":
        streamHandler = logging.StreamHandler(stream = sys.stdout)
        streamHandler.setLevel(logging.INFO)
        fileHandler.setLevel(logging.INFO)
        logger.setLevel(logging.INFO)
    if LogLevel == "ERROR":
        streamHandler = logging.StreamHandler(stream = sys.stderr)
        streamHandler.setLevel(logging.ERROR)
        fileHandler.setLevel(logging.ERROR)
        logger.setLevel(logging.ERROR)

    streamHandler.setFormatter(logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s', datefmt = '%Y/%m/%d %H:%M:%S'))
    if WriteToStream:
        logger.addHandler(streamHandler)           
    logger.addHandler(fileHandler)
    return logger
