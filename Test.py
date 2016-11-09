 # -*- coding:utf-8 -*-
__author__ = "Wang Hewen"
import numpy as np
import CommonModules.DataStructureOperations
import CommonModules.IO
from CommonModules.Utilities import TimeElapsed

CM = CommonModules

def main():
    print(TimeElapsed())
    test_array = np.array([[4,5,6]])
    #test_array = np.array([])
    print(CM.DataStructureOperations.CombineMatricesRowWise(test_array, np.array([[1,2,3]])))
    #CM.IO.ExportNpArray("./test.txt", test_array)
    print(TimeElapsed(LastTime = True))
    return

if __name__ == "__main__":
    main()