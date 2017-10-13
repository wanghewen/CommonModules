# -*- coding:utf-8 -*-
"""Provided data structure related operations such as remove row from matrix."""

__author__ = "Wang Hewen"

import itertools
DependencyFlag = False #Check if dependencies are satisfied. If not, some advanced functions will not be defined.
try:
    import scipy.sparse
    import numpy as np
    DependencyFlag = True
except Exception:
    DependencyFlag = False

def FlattenList(List):
    '''
    Flatten a list using itertools no matter how many nest it has. 
    E.g. [['foo', 'baz'], ['gg']] or [[['foo', 'baz'], ['gg']]] to ['foo', 'baz', 'gg'].

    :param List[Variant]: The list you want to flatten
    :return: List: Flattened list
    :rtype: List[Variant]
    '''
    for Element in List:
        if type(Element)==list:
            List = list(itertools.chain(*List))
            return FlattenList(List)
    return list(List)

if DependencyFlag:
    def CombineMatricesRowWise(MainMatrix, AddedMatrix, RemoveFirstZerosRow = True, Sparse = False):
        '''
        Stack twoe matrices vertically (row wise).
        You must make sure MainMatrix and AddedMatrix have appropriate dimensions, i.e. have same number of columns.
    
        :param SparseMatrix MainMatrix: The main matrix that you want to add the AddedMatrix.
        :param SparseMatrix AddedMatrix: The matrix added followed by the main matrix.
        :param Boolean RemoveFirstZerosRow: When MainMatrix is empty, this method will automatically add a row with all zeros in the first row of MainMatirx. When this is True, Result will auto remove the first all zeros row when returns. Otherwise you need to manually do it.
        :param Boolean Sparse: If Sparse is True, the matrix will be automatically converted to sparse matrix and it's less space consuming and slower.
        :return: Result: The result of Stacking matrices vertically (row wise).
        :rtype: NumpyArray/SparseMatrix
        '''
        MainMatrixInitialSize = MainMatrix.size
        MainMatrixInitialShape = MainMatrix.shape[0]

        if Sparse == True:
            if MainMatrixInitialSize == 0:
                MainMatrix = scipy.sparse.csr_matrix([np.zeros(AddedMatrix.shape[1], dtype = int)])
            elif MainMatrixInitialShape == 1:#Need to do this conversion otherwise will return error
                MainMatrix = scipy.sparse.csr_matrix(MainMatrix)

            Result = scipy.sparse.vstack([MainMatrix, AddedMatrix], format = "csr")
        else:
            if MainMatrixInitialSize == 0:
                MainMatrix = np.array([np.zeros(AddedMatrix.shape[1], dtype = int)])

            Result = np.vstack((MainMatrix, AddedMatrix))

        if MainMatrixInitialSize == 0 and RemoveFirstZerosRow:
            Result = Result[1:]

        return Result


    def CombineSparseMatricesRowWise(MainMatrix, AddedMatrix, RemoveFirstZerosRow = True):
        '''
        Stack two scipy sparse matrices vertically (row wise). Will initialize the main matrix to be two dimensional csr_matrix with all zero elements if the main matrix is empty.
        You can use .toarray() to convert final result to numpy array(not a sparse matrix)
        You must make sure MainMatrix and AddedMatrix have appropriate dimensions, i.e. have same number of columns.
    
        :param SparseMatrix MainMatrix: The main matrix that you want to add the AddedMatrix.
        :param SparseMatrix AddedMatrix: The matrix added followed by the main matrix.
        :param Boolean RemoveFirstZerosRow: When MainMatrix is empty, this method will automatically add a row with all zeros in the first row of MainMatirx. When this is True, Result will auto remove the first all zeros row when returns. Otherwise you need to manually do it.
        :return: Result: The result of Stacking sparse matrices vertically (row wise).
        :rtype: SparseMatrix
        '''
        return CombineMatricesRowWise(MainMatrix, AddedMatrix, RemoveFirstZerosRow, Sparse = True)

    def DeleteLilMatrixRow(mat, i):
        '''
        Delete a row in a scipy.sparse.lil_matrix.

        :param scipy.sparse.lil_matrix mat: The scipy.sparse.lil_matrix you want to operate on.
        :param Int i: The row number that you want to delete
        :return: SparseMatrix mat: The result of deleted sparse matrix.
        :rtype: SparseMatrix
        '''

        if not isinstance(mat, scipy.sparse.lil.lil_matrix):
            #print mat.__class__
            raise ValueError("works only for LIL format -- use .tolil() first")
        mat.rows = np.delete(mat.rows, i)
        mat.data = np.delete(mat.data, i)
        mat._shape = (mat._shape[0] - 1, mat._shape[1])

        return mat

    def DeleteCsrMatrixRow(mat, i):
        '''
        Delete a row in a scipy.sparse.csr_matrix.

        :param scipy.sparse.csr_matrix mat: The scipy.sparse.csr_matrix you want to operate on.
        :param Int i: The row number that you want to delete
        :return: SparseMatrix mat: The result of deleted sparse matrix.
        :rtype: SparseMatrix
        '''
        if not isinstance(mat, scipy.sparse.csr_matrix):
            try:
                print("Warning: works only for CSR format -- use .tocsr() first")
                mat = mat.tocsr()
            except:
                raise ValueError("cannot convert mat to CSR format")
            #raise ValueError("works only for CSR format -- use .tocsr() first")
        n = mat.indptr[i+1] - mat.indptr[i]
        if n > 0:
            mat.data[mat.indptr[i]:-n] = mat.data[mat.indptr[i+1]:]
            mat.data = mat.data[:-n]
            mat.indices[mat.indptr[i]:-n] = mat.indices[mat.indptr[i+1]:]
            mat.indices = mat.indices[:-n]
        mat.indptr[i:-1] = mat.indptr[i+1:]
        mat.indptr[i:] -= n
        mat.indptr = mat.indptr[:-1]
        mat._shape = (mat._shape[0]-1, mat._shape[1])

        return mat

    def IfTwoSparseMatrixEqual(SparseMatrix1, SparseMatrix2):
        '''
        Check if two scipy sparse matrix is exactly the same.
    
        :param SparseMatrix SparseMatrix1: The first scipy sparse matrix.
        :param SparseMatrix SparseMatrix2: The second scipy sparse matrix.
        :return: Equal: True if they are equal, otherwise will be false.
        :rtype: Boolean
        '''
        if (SparseMatrix1 - SparseMatrix2).nnz == 0:
            return True
        else:
            return False
