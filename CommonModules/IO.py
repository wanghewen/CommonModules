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
import zipfile

def ListApkFiles(ApkDirectory):
    '''
Get the Apk file names for an ApkDirectory in a sorted order. Rerurn an empty list if ApkDirectory=="".

:param String ApkDirectory: Path of a apk file directory
:return: ListOfApkFiles: The list of Paths of Apks under ApkDirectory
:rtype: List[String]
    '''
    ListOfApkFiles=[]
    if(ApkDirectory==""):
        raise ValueError('Directory is empty!')
    filenames = os.listdir(ApkDirectory)
    for filename in filenames:
        #list filenames 
        #get the Path for the files
        Path=os.path.abspath(os.path.join(ApkDirectory, filename))
        #get the Path for the files
        if os.path.splitext(filename)[1]==".apk":
            if os.path.isfile(Path):
                ListOfApkFiles.append(Path)
    return sorted(ListOfApkFiles)

def ListFiles(Directory, Extension):
    '''
    Given an extension, get the file names for a Directory in a sorted order. Rerurn an empty list if Directory == "".

    :param String/List Directory: Path/Paths of a file directory
    :param String Extension: Extension of the files you want. Better include "." in the Extension. Use "." to list all files.
    :return: ListOfFiles: The list of Paths of the files you want under Directory
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
                    #get the Path for the files
                    Path=os.path.abspath(os.path.join(Directory, filename))
                    #get the Path for the files
                    if os.path.splitext(filename)[1]==Extension or Extension == ".":
                        if os.path.isfile(Path):
                            ListOfFiles.append(Path)
    else:
        filenames = os.listdir(Directory)
        for filename in filenames:
            #list filenames 
            #get the Path for the files
            Path=os.path.abspath(os.path.join(Directory, filename))
            #get the Path for the files
            if os.path.splitext(filename)[1]==Extension:
                if os.path.isfile(Path):
                    ListOfFiles.append(Path)
    return sorted(ListOfFiles)

def ListAllFiles(Directory, Extension):
    '''
    Given an extension, get the file names for a Directory and all its sub-directories in a sorted order. Rerurn an empty list if Directory == "".

    :param String Directory: Path of a file directory
    :param String Extension: Extension of the files you want. Better include "." in the Extension. Use "." to list all files.
    :return: ListOfFiles: The list of Paths of the files you want under Directory
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
            #get the Path for the files
            Path = os.path.join(root, filename)
            #get the Path for the files
            if os.path.splitext(filename)[1] == Extension or Extension == ".":
                if os.path.isfile(Path):
                    ListOfFiles.append(Path)
    return sorted(ListOfFiles)

def ListDirs(Directory):
    '''
    Get all sub-directory paths for a Directory in a sorted order. Rerurn an empty list if Directory == "". Modified from ListFiles(which means variable names remain the same...)

    :param String Directory: Path of a file directory
    :return: ListOfFiles: The list of Paths of the sub-directories you want under the Directory
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
        #get the Path for the files
        Path=os.path.abspath(os.path.join(Directory, filename))
        #get the Path for the files
        if os.path.isdir(Path):
            ListOfFiles.append(Path)
    return sorted(ListOfFiles)
    
    
def FileExist(FilePath):
    '''
    Given file path, determine a file exist or not.

    :param String FilePath: Path of a file or directory
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

    :param String Folder: Path of a directory
    :rtype: Boolean
    '''
    if(FileExist(Folder) == False):
        raise IOError("Directory not found!")
    else:
        shutil.rmtree(Folder)

def ExportToJson(Path, Content):
    '''
    Export something to json file. 
    Will automatic convert Set content into List.

    :param String Path: Path to store the json file
    :param Variant Content: something you want to export
    '''
    if(isinstance(Content,set)):
        Content = list(Content)
    #if(isinstance(Content, collections.defaultdict)):
    #    Content = dict(Content)
    with open(Path, "w", encoding = "utf8") as f:
        json.dump(Content, f, indent=4)


def ExportToPkl(Path,Content):
    '''
    Export something to pickle file. 
    Will automatic convert Set content into List.

    :param String Path: Path to store the json file
    :param Variant Content: something you want to export
    '''
    if(isinstance(Content, set)):
        Content = list(Content)
    #if(isinstance(Content, collections.defaultdict)):
    #    Content = dict(Content)
    with open(Path, "wb") as fd:
        pickle.dump(Content, fd)

def ImportFromPkl(Path):
    '''
    Import something from pickle file. 

    :param String Path: Path of the pickle file
    :return: Content: Content in the pickle file
    :rtype: Variant
    '''    
    with open(Path,"rb") as fd:
        Content = pickle.load(fd)
    return Content

def ExportToJsonNodeLinkData(Path,GraphContent):
    '''
    Export graph node link date to json file. 

    :param String Path: Path to store the json file
    :param nxGraph GraphContent: some graph you want to export
    '''    
    with open(Path,"wb") as f:
        Content=json_graph.node_link_data(GraphContent)
        json.dump(Content, f, indent=4)


def ExportToGML(Path, GraphContent):
    '''
    Export graph node link date to json file. 

    :param String Path: Path to store the json file
    :param nxGraph GraphContent: some graph you want to export
    '''    
    nx.write_gml(GraphContent, Path)


def ImportFromJsonNodeLinkData(Path):
    '''
    Import graph node link date from json file.

    :param String Path: Path of the json file
    :return: GraphContent: Graph content in the json file
    :rtype: nxGraph
    '''    
    with open(Path,"rb") as f:
        Content=json.load(f)
        GraphContent=json_graph.node_link_graph(Content)

        return GraphContent

def ImportFromJson(Path):
    '''
    Import something from json file. 

    :param String Path: Path of the json file
    :return: Content: Content in the json file
    :rtype: Variant
    '''    
    with open(Path,"r") as File:
        Content=json.load(File, encoding = "utf-8")
        return Content
def ExportNpArray(Path, NpArray, Format = "%f"):
    '''
    Export a Numpy array to a file.
    
    :param String Path: The stored file location.
    :param numpy.array NpArray: The Numpy array you want to store.
    :param String Format: How to print each element, e.g. %i, %10.5f
    '''

    np.savetxt(Path, NpArray, fmt = Format)

def ImportNpArray(Path, DataType, ndmin = 0):
    '''
    Import a Numpy array from a file.
    
    :param String Path: The stored file location.
    :param data-type DataType: How to match each element, e.g. int, float
    :param int ndmin: How many dimensions of array at least you will have.
    :return: NpArray: NpArray in the file
    :rtype: NpArray
    '''
    NpArray = np.loadtxt(Path, dtype = DataType, ndmin = ndmin)
    return NpArray

def ExportSparseMatrix(Path, SparseMatrix):
    '''
    Export a scipy sparse matrix to a file using matrix market format.
    Please refer to http://math.nist.gov/MatrixMarket/formats.html for more information about this format.
    
    :param String Path: The stored file location.
    :param scipy sparse matrix SparseMatrix: The scipy sparse matrix you want to store.
    '''
    with open(Path, "wb+") as File:
        scipy.io.mmwrite(File, SparseMatrix)

def ImportSparseMatrix(Path):
    '''
    Import a scipy sparse matrix from a file using matrix market format.
    
    :param String Path: The stored file location.
    :return: SparseMatrix: (converted) scipy csr_matrix in the file
    :rtype: Scipy Sparse Matrix
    '''
    SparseMatrix = scipy.io.mmread(Path)
    SparseMatrix = SparseMatrix.tocsr()
    return SparseMatrix

def CompressFiles(Paths, CompressedFilePath, Format = "zip"):
    '''
    Compress files into a (zip) file.
    
    :param List Paths: Paths of the files you want to compress. These paths will be under the root of the compressed file.(You may want to use ListFiles to pass in all paths)
    :param String CompressedFilePath: Path of the compressed file you want to store.
    :param String Format: The format of the compressed file.
    '''
    if Format == "zip":        
        CompressedFile = zipfile.ZipFile(CompressedFilePath, "w", compression = zipfile.ZIP_DEFLATED)
        for Path in Paths:
            parent_folder = os.path.dirname(Path)
            if os.path.isdir(Path):
                for root, folders, files in os.walk(Path):
                    # Include all subfolders, including empty ones.
                    for folder_name in folders:
                        absolute_path = os.path.join(root, folder_name)
                        relative_path = absolute_path.replace(parent_folder, '')
                        CompressedFile.write(absolute_path, relative_path)
                    for file_name in files:
                        absolute_path = os.path.join(root, file_name)
                        relative_path = absolute_path.replace(parent_folder, '')
                        CompressedFile.write(absolute_path, relative_path)
            else:
                relative_path = os.path.split(Path)[-1]
                CompressedFile.write(Path, relative_path)
        CompressedFile.close()
    else:
        raise NotImplementedError


def DecompressFiles(Paths, TargetFolder, Format = "zip"):
    '''
    Decompress files from a (zip) file/files.
    
    :param List Paths: Paths of the files you want to decompress. 
    :param String TargetFolder: Path of the decompressed files you want to store.
    :param String Format: The format of the compressed file.
    '''
    if Format == "zip":        
        for Path in Paths:
            CompressedFile = zipfile.ZipFile(Path, "r")
            CompressedFile.extractall(TargetFolder)
            CompressedFile.close()
    else:
        raise NotImplementedError