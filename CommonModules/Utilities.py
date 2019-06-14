 # -*- coding:utf-8 -*-
__author__ = "Wang Hewen"
""" Some other functionalities."""
import datetime
import time
import shutil

global CurrentTime
global StartTime
CurrentTime = 0
StartTime = 0

def ConvertTimeStampToDateTime(TimeStamp, TimeType = 0, ReturnType = 0):
    '''
    Convert a time stamp(seconds since epoch) to a Python datetime object.
    
    :param Number/String TimeStamp: A time stamp(seconds since epoch).
    :param Number TimeType: Type 0 means the same time zone as current computer. Type 1 means UTC time.
    :param Number ReturnType: ReturnType 0 means datetime object. ReturnType 1 means time.struct_time object, which can be used like a tuple.
    :return: DateTimeObjcet/DateTimeObject.timetuple():
    :rtype: datetime object/time.struct_time object
    '''
    TimeStamp = float(TimeStamp)
    if TimeType  == 0:
        DateTimeObject = datetime.datetime.fromtimestamp(TimeStamp)
    elif TimeType == 1:
        DateTimeObject = datetime.datetime.utcfromtimestamp(TimeStamp)
    else:
        raise ValueError("Incorrect TimeType.")
    if ReturnType == 0:
        return DateTimeObject
    elif ReturnType == 1:
        return DateTimeObject.timetuple()
    else:
        raise ValueError("Incorrect ReturnType.")


def ConcatenateIntegers(*Integers):
    '''
    Concatenate/Merge integers into one integer. E.g. 10 and 20 to 1020.

    :param Integers Integers: Integers to be concatenated.
    :return: Result: Concatenated integer.
    :rtype: Integer
    '''
    Result = ''
    for Integer in Integers:
        Result += str(Integer)
    return int(Result)

def TimeElapsed(Unit = True, LastTime = False):
    '''
    Return the time interval since first/last call of this function.

    :param Boolean/String Unit: Whether to append unit ' sec'(by default) or other unit when returned. If False, a float number will be returned.
    :param Boolean LastTime: If True return the time interval since the last call of this function, otherwise return the time interval since the first call of this function, e.g. since programming running.
    :return: TimeInterval: Time interval since last call of this function..
    :rtype: String/Float
    '''
    global CurrentTime
    global StartTime

    if LastTime:
        TimeInterval = time.time() - CurrentTime#Basically it's the previous time
    else:
        TimeInterval = time.time() - StartTime

    if StartTime == 0:
        TimeInterval = 0.0
        StartTime = time.time()

    CurrentTime = time.time()
    
    if Unit == True:
        return str(TimeInterval) + " sec"
    elif Unit:
        return str(TimeInterval) + Unit
    else:
        return TimeInterval

def GetHardDiskUsage(Print = True):
    '''
    Use shutil to obtain hard disk usage.

    :param Boolean Print: Whether to use print function to print disk usage on the screen.
    :return: DiskUsage: A tuple contains total, used and free disk space in bytes.
    :rtype: Tuple
    '''
    total, used, free = shutil.disk_usage("/")
    if Print:
        print("Total: %d GB" % (total // (2 ** 30)))
        print("Used: %d GB" % (used // (2 ** 30)))
        print("Free: %d GB" % (free // (2 ** 30)))

    return total, used, free
