# -*- coding:utf-8 -*-

"""File I/O related operations, such as list files, import/export or remove files/folder."""

__author__ = "Wang Hewen"

import os
import shutil
import json
import pickle
import zipfile
import urllib
import wget

DependencyFlag = False #Check if dependencies are satisfied. If not, some advanced functions will not be defined.
try:
    import networkx as nx
    from networkx.readwrite import json_graph
    import numpy as np
    import scipy.io
    DependencyFlag = True
except Exception:
    DependencyFlag = False

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

def ListFiles(Directory, Extension, All = False):
    '''
    Given an extension, get the file names for a Directory in a sorted order. Rerurn an empty list if Directory == "".

    :param String/List Directory: Path/Paths of a file directory
    :param String Extension: Extension of the files you want. Better include "." in the Extension. Use "." to list all files. Use ""(empty string) to list all folders.
    :param Boolean All: Whether to include all files in sub-directories
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
        if All:
            for Directory in Directories:
                ListOfFiles.extend(_ListAllFiles(Directory, Extension))
        else:
            for Directory in Directories:
                    filenames = os.listdir(Directory)
                    for filename in filenames:
                        #list filenames 
                        #get the Path for the files
                        Path=os.path.abspath(os.path.join(Directory, filename))
                        #get the Path for the files
                        if Extension == "": #Need to get all folders instead of files
                            if os.path.isdir(Path):
                                ListOfFiles.append(Path)
                        else:
                            if os.path.splitext(filename)[1]==Extension or Extension == ".":
                                if os.path.isfile(Path):
                                    ListOfFiles.append(Path)
    else:
        if All:
            ListOfFiles = _ListAllFiles(Directory, Extension)
        else:
            filenames = os.listdir(Directory)
            for filename in filenames:
                #list filenames 
                #get the Path for the files
                Path=os.path.abspath(os.path.join(Directory, filename))
                #get the Path for the files
                if Extension == "": #Need to get all folders instead of files
                    if os.path.isdir(Path):
                        ListOfFiles.append(Path)
                else:
                    if os.path.splitext(filename)[1]==Extension or Extension == ".":
                        if os.path.isfile(Path):
                            ListOfFiles.append(Path)
    return sorted(ListOfFiles)

def _ListAllFiles(Directory, Extension):
    '''
    Given an extension, get the file names for a Directory and all its sub-directories in a sorted order. Rerurn an empty list if Directory == "".

    :param String Directory: Path of a file directory
    :param String Extension: Extension of the files you want. Better include "." in the Extension. Use "." to list all files. Use ""(empty string) to list all folders.
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
        if Extension == "":#Need to get all folders instead of files
            ListOfFiles.append(os.path.abspath(root))
        else:
            for filename in files:
                #list filenames 
                #get the Path for the files
                Path = os.path.abspath(os.path.join(root, filename))
                #get the Path for the files
                if os.path.splitext(filename)[1] == Extension or Extension == ".":
                    if os.path.isfile(Path):
                        ListOfFiles.append(Path)
    if Extension == "":
        ListOfFiles = ListOfFiles[1:] #Remove Directory in the list since the list contains the path of Directory itself
    return sorted(ListOfFiles)

    
def CopyFolderStructure(SourceFolder, DestinationFolder, Root = False):
    '''
    Copy a folder structure without copying any of the files inside of it.

    :param String Directory: Path of the source folder
    :param String Directory: Path of the destination folder that the source folder structure will be copied
    :param Boolean Root: DestinationAsRoot. If this is True, the DestinationFolder will be ragarded as a folder of the same level of SourceFolder, otherwise SourceFolder will be copied into the DestinationFolder
    '''
    ListOfFolders = ListFiles(SourceFolder, "", All = True)
    os.makedirs(DestinationFolder, exist_ok = True)
    if Root is False:
        for Folder in ListOfFolders:
            os.makedirs(os.path.join(DestinationFolder, os.path.split(SourceFolder)[-1], os.path.relpath(Folder, SourceFolder)), exist_ok = True)
    else:
        for Folder in ListOfFolders:
            os.makedirs(os.path.join(DestinationFolder, os.path.relpath(Folder, SourceFolder)), exist_ok = True)

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

def DownloadFile(URL, Destination = "./download", ExpectedBytes = None, IsDestinationFolder = None):
    """
    Download a file if not present, and make sure it's the right size.

    :param String URL: URL of the file you want to download.
    :param String Destination: Path of the file you want to store, it can be a.
    :param String Format: The format of the compressed file.
    """
    if IsDestinationFolder is None: #Try to indicate from Destination
        if os.path.basename(Destination).find(".") >= 0:
            IsDestinationFolder = False
        else:
            IsDestinationFolder = True
    if IsDestinationFolder is True:
        if os.path.isdir(Destination):
            pass
        else:
            os.makedirs(Destination)

    Request = urllib.request.Request(URL, method = "HEAD")
    Headers = dict(urllib.request.urlopen(Request).info().items())
    if IsDestinationFolder:
        FilePath = os.path.join(Destination, wget.detect_filename(URL, '', Headers))
    else:
        FilePath = wget.detect_filename(URL, Destination, Headers)

    if not os.path.exists(FilePath):
        FileName = wget.download(URL, Destination)
    else:
        FileName = FilePath
    StatInfo = os.stat(FileName)
    if ExpectedBytes is None or StatInfo.st_size == ExpectedBytes:
        print('Found and verified', FileName)
    else:
        print(StatInfo.st_size)
        raise FileExistsError(
            'Failed to verify ' + FileName + '. File exists or corrupted. Can you get to it with a browser?')
    return FileName


if DependencyFlag:
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