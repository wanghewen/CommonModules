 # -*- coding:utf-8 -*-
__author__ = "Wang Hewen"
import numpy as np
import CommonModules.DataStructureOperations as DSO
import CommonModules.IO as IO

def main():
    test_array = np.array([[4,5,6]])
    #test_array = np.array([])
    print(DSO.CombineSparseMatricesRowWise(test_array, np.array([[1,2,3]])).toarray())
    IO.ExportNpArray("./test.txt", test_array)
    return

if __name__ == "__main__":
    main()