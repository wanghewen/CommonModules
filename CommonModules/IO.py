# -*- coding:utf-8 -*-

"""File I/O related operations, such as list files, import/export or remove files/folder."""

__author__ = "Wang Hewen"

import os
import shutil
import json
import pickle
import networkx as nx
from networkx.readwrite import json_graph
import numpy as np
import scipy.io

def ListApkFiles(ApkDirectory):
    '''
Get the Apk file names for an ApkDirectory in a sorted order. Rerurn an empty list if ApkDirectory=="".

:param String ApkDirectory: absolute path of a apk file directory
:return: ListOfApkFiles: The list of absolute paths of Apks under ApkDirectory
:rtype: List[String]
    '''
    ListOfApkFiles=[]
    if(ApkDirectory==""):
        raise ValueError('Directory is empty!')
    filenames = os.listdir(ApkDirectory)
    for filename in filenames:
        #list filenames 
        #get the absolute path for the files
        AbsolutePath=os.path.abspath(os.path.join(ApkDirectory, filename))
        #get the absolute path for the files
        if os.path.splitext(filename)[1]==".apk":
            if os.path.isfile(AbsolutePath):
                ListOfApkFiles.append(AbsolutePath)
    return sorted(ListOfApkFiles)

def ListFiles(Directory, Extension):
    '''
    Given an extension, get the file names for a Directory in a sorted order. Rerurn an empty list if Directory == "".

    :param String Directory: absolute path of a file directory
    :param String Extension: Extension of the files you want. Better include "." in the Extension
    :return: ListOfFiles: The list of absolute paths of the files you want under Directory
    :rtype: List[String]
    '''
    ListOfFiles=[]
    if(Directory == "" or Directory == []):
        return []
    if(type(Directory) != list and os.path.isdir(Directory) == False):
        raise ValueError(Directory, 'Directory is not a directory!')
    if(type(Extension)!=str):
        raise ValueError(Extension, 'Extension is not a string!')
    if(Extension):
        if(Extension[0] != "."):
            Extension = "." + Extension
    if type(Directory) == list:
        Directories = Directory
        for Directory in Directories:
                filenames = os.listdir(Directory)
                for filename in filenames:
                    #list filenames 
                    #get the absolute path for the files
                    AbsolutePath=os.path.abspath(os.path.join(Directory, filename))
                    #get the absolute path for the files
                    if os.path.splitext(filename)[1]==Extension:
                        if os.path.isfile(AbsolutePath):
                            ListOfFiles.append(AbsolutePath)
    else:
        filenames = os.listdir(Directory)
        for filename in filenames:
            #list filenames 
            #get the absolute path for the files
            AbsolutePath=os.path.abspath(os.path.join(Directory, filename))
            #get the absolute path for the files
            if os.path.splitext(filename)[1]==Extension:
                if os.path.isfile(AbsolutePath):
                    ListOfFiles.append(AbsolutePath)
    return sorted(ListOfFiles)

def ListAllFiles(Directory, Extension):
    '''
    Given an extension, get the file names for a Directory and all its sub-directories in a sorted order. Rerurn an empty list if Directory == "".

    :param String Directory: absolute path of a file directory
    :param String Extension: Extension of the files you want. Better include "." in the Extension
    :return: ListOfFiles: The list of absolute paths of the files you want under Directory
    :rtype: List[String]
    '''
    ListOfFiles=[]
    if(Directory == ""):
        raise ValueError(Directory, 'Directory is empty!')
    if(os.path.isdir(Directory) == False):
        raise ValueError(Directory, 'Directory is not a directory!')
    if(type(Extension)!=str):
        raise ValueError(Extension, 'Extension is not a string!')
    if(Extension):
        if(Extension[0] != "."):
            Extension = "." + Extension
    for root, dirs, files in os.walk(Directory):
        for filename in files:
            #list filenames 
            #get the absolute path for the files
            AbsolutePath = os.path.join(root, filename)
            #get the absolute path for the files
            if os.path.splitext(filename)[1] == Extension:
                if os.path.isfile(AbsolutePath):
                    ListOfFiles.append(AbsolutePath)
    return sorted(ListOfFiles)

def ListDirs(Directory):
    '''
    Get all sub-directory paths for a Directory in a sorted order. Rerurn an empty list if Directory == "". Modified from ListFiles(which means variable names remain the same...)

    :param String Directory: absolute path of a file directory
    :return: ListOfFiles: The list of absolute paths of the sub-directories you want under the Directory
    :rtype: List[String]
    '''
    ListOfFiles=[]
    if(Directory == ""):
        raise ValueError(Directory, 'Directory is empty!')
    if(os.path.isdir(Directory) == False):
        raise ValueError(Directory, 'Directory is not a directory!')
    filenames = os.listdir(Directory)
    for filename in filenames:
        #list filenames 
        #get the absolute path for the files
        AbsolutePath=os.path.abspath(os.path.join(Directory, filename))
        #get the absolute path for the files
        if os.path.isdir(AbsolutePath):
            ListOfFiles.append(AbsolutePath)
    return sorted(ListOfFiles)
    
    
def FileExist(FilePath):
    '''
    Given file path, determine a file exist or not.

    :param String FilePath: absolute path of a file or directory
    :rtype: Boolean
    '''
    if os.path.exists(FilePath)==True:
        return True
    else:
        #if os.path.isdir(ApkFilePath)==False:
        #    if(os.path.basename(ApkFilePath)) in os.listdir(os.getcwd()):
        #        return True
        return False

def RemoveDirectory(Folder):
    '''
    Given Folder path, remove this folder(include all content inside).

    :param String Folder: absolute path of a directory
    :rtype: Boolean
    '''
    if(FileExist(Folder) == False):
        raise IOError("Directory not found!")
    else:
        shutil.rmtree(Folder)

def ExportToJson(AbsolutePath, Content):
    '''
    Export something to json file. 
    Will automatic convert Set content into List.

    :param String AbsolutePath: absolute path to store the json file
    :param Variant Content: something you want to export
    '''
    if(isinstance(Content,set)):
        Content = list(Content)
    #if(isinstance(Content, collections.defaultdict)):
    #    Content = dict(Content)
    with open(AbsolutePath, "w", encoding = "utf8") as f:
        json.dump(Content, f, indent=4)


def ExportToPkl(AbsolutePath,Content):
    '''
    Export something to pickle file. 
    Will automatic convert Set content into List.

    :param String AbsolutePath: absolute path to store the json file
    :param Variant Content: something you want to export
    '''
    if(isinstance(Content, set)):
        Content = list(Content)
    #if(isinstance(Content, collections.defaultdict)):
    #    Content = dict(Content)
    with open(AbsolutePath, "wb") as f:
        pickle.dump(Content, f)

def ImportFromPkl(AbsolutePath):
    '''
    Import something from pickle file. 

    :param String AbsolutePath: absolute path of the pickle file
    :return: Content: Content in the pickle file
    :rtype: Variant
    '''    
    with open(AbsolutePath,"rb") as File:
        Content = pickle.load(File)


def ExportToJsonNodeLinkData(AbsolutePath,GraphContent):
    '''
    Export graph node link date to json file. 

    :param String AbsolutePath: absolute path to store the json file
    :param nxGraph GraphContent: some graph you want to export
    '''    
    with open(AbsolutePath,"wb") as f:
        Content=json_graph.node_link_data(GraphContent)
        json.dump(Content, f, indent=4)


def ExportToGML(AbsolutePath, GraphContent):
    '''
    Export graph node link date to json file. 

    :param String AbsolutePath: absolute path to store the json file
    :param nxGraph GraphContent: some graph you want to export
    '''    
    nx.write_gml(GraphContent, AbsolutePath)


def ImportFromJsonNodeLinkData(AbsolutePath):
    '''
    Import graph node link date from json file.

    :param String AbsolutePath: absolute path of the json file
    :return: GraphContent: Graph content in the json file
    :rtype: nxGraph
    '''    
    with open(AbsolutePath,"rb") as f:
        Content=json.load(f)
        GraphContent=json_graph.node_link_graph(Content)

        return GraphContent

def ImportFromJson(AbsolutePath):
    '''
    Import something from json file. 

    :param String AbsolutePath: absolute path of the json file
    :return: Content: Content in the json file
    :rtype: Variant
    '''    
    with open(AbsolutePath,"r") as File:
        Content=json.load(File, encoding = "utf-8")
        return Content
def ExportNpArray(AbsolutePath, NpArray, Format = "%f"):
    '''
    Export a Numpy array to a file.
    
    :param String AbsolutePath: The stored file location.
    :param numpy.array NpArray: The Numpy array you want to store.
    :param String Format: How to print each element, e.g. %i, %10.5f
    '''

    np.savetxt(AbsolutePath, NpArray, fmt = Format)

def ImportNpArray(AbsolutePath, DataType, ndmin = 0):
    '''
    Import a Numpy array from a file.
    
    :param String AbsolutePath: The stored file location.
    :param data-type DataType: How to match each element, e.g. int, float
    :param int ndmin: How many dimensions of array at least you will have.
    :return: NpArray: NpArray in the file
    :rtype: NpArray
    '''
    NpArray = np.loadtxt(AbsolutePath, dtype = DataType, ndmin = ndmin)
    return NpArray

def ExportSparseMatrix(AbsolutePath, SparseMatrix):
    '''
    Export a scipy sparse matrix to a file using matrix market format.
    Please refer to http://math.nist.gov/MatrixMarket/formats.html for more information about this format.
    
    :param String AbsolutePath: The stored file location.
    :param scipy sparse matrix SparseMatrix: The scipy sparse matrix you want to store.
    '''
    with open(AbsolutePath, "wb+") as File:
        scipy.io.mmwrite(File, SparseMatrix)

def ImportSparseMatrix(AbsolutePath):
    '''
    Import a scipy sparse matrix from a file using matrix market format.
    
    :param String AbsolutePath: The stored file location.
    :return: SparseMatrix: (converted) scipy csr_matrix in the file
    :rtype: Scipy Sparse Matrix
    '''
    SparseMatrix = scipy.io.mmread(AbsolutePath)
    SparseMatrix = SparseMatrix.tocsr()
    return SparseMatrix