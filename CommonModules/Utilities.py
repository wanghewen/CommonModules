 # -*- coding:utf-8 -*-
__author__ = "Wang Hewen"
""" Some other functionalities."""
import datetime

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
