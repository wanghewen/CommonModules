# -*- coding:utf-8 -*-
""" Provide log related functions. When importing this module, 
the logging file named LogFile.log will be automatically created in 
the current working directory.
You can use from Log import logger to use the logger.
E.g. 
logger.error("Pickle data writing Failed.")
logger.info("Pickle data of " + foo + " written successfully.")  
"""

__author__ = "Wang Hewen"

import sys
import logging
logging.basicConfig(level=logging.DEBUG,filename="LogFile.log",filemode="a",
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s',
                    datefmt='%Y/%m/%d %H:%M:%S')
ErrorHandler = logging.StreamHandler(stream = sys.stderr)
ErrorHandler.setLevel(logging.ERROR)
DebugHandler = logging.StreamHandler(stream = sys.stdout)
DebugHandler.setLevel(logging.DEBUG)
ErrorHandler.setFormatter(logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s'))
DebugHandler.setFormatter(logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s'))

logger = logging.getLogger()
logger.addHandler(ErrorHandler)
logger.addHandler(DebugHandler)

