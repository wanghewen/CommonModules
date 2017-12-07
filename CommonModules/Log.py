# -*- coding:utf-8 -*-
""" Provide log related functions. You need to Initialize the logger and use the logger to make logs.
E.g. 
logger = Initialize()
logger.error("Pickle data writing Failed.")
logger.info("Pickle data of " + foo + " written successfully.")  
"""

__author__ = "Wang Hewen"

import sys
import logging

def Initialize(FileName = "LogFile.log", LogLevel = "INFO", WriteToStream = False):
    if LogLevel not in ["DEBUG", "INFO", "ERROR"]:
        raise ValueError("LogLevel is not correctly set.")
    logger = logging.getLogger(__name__) #__name__ == CommonModules.Log
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
