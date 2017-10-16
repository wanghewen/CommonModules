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

def Initialize(FileName = "LogFile.log", LogLevel = "INFO"):
    if LogLevel not in ["DEBUG", "INFO", "ERROR"]:
        raise ValueError("LogLevel is not correctly set.")
    logging.basicConfig(level = logging.DEBUG, filename = FileName, filemode = "a",
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s',
                        datefmt='%Y/%m/%d %H:%M:%S')
    logger = logging.getLogger()
    if LogLevel in ["DEBUG"]:
        DebugHandler = logging.StreamHandler(stream = sys.stdout)
        DebugHandler.setLevel(logging.DEBUG)
        DebugHandler.setFormatter(logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s'))
        logger.addHandler(DebugHandler)
    if LogLevel in ["DEBUG", "INFO"]:
        InfoHandler = logging.StreamHandler(stream = sys.stdout)
        InfoHandler.setLevel(logging.INFO)
        InfoHandler.setFormatter(logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s'))
        logger.addHandler(InfoHandler)
    if LogLevel in ["DEBUG", "INFO", "ERROR"]:
        ErrorHandler = logging.StreamHandler(stream = sys.stderr)
        ErrorHandler.setLevel(logging.ERROR)
        ErrorHandler.setFormatter(logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s'))
        logger.addHandler(ErrorHandler)           

    return logger
