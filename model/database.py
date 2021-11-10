import os

from utils import *

class Database:
    __path = "" 
    __imagesPaths = []
    __vectors = None
    __name = ""
    __savePath = ""
    __size = 0


    def __init__(self, name, path, savePath):
        self.__name = name
        self.__path = path 
        self.__savePath = savePath + "/" + self.__name + ".npy" 

        #generate array containing the paths of all the entries on our database
        tmp = self._generateImageNames(self.__path)
        self.__imagesPaths = tmp[0]
        self.__size = tmp[1]

        #check wether the database is already saved
        if self.__savePath.is_file():
            self.__vectors = np.load(str(self.__savePath))
        else:
            self.__vectors = self._generateVectors(self.__imagesPaths, self.__size)
            
    # args: path of the database
    # return: array with the paths of all elements in the databse (png and/or jpg)
    def _generateImageNames(self, path):
        output = []
        size = 0
        for entry in os.scandir(path):
            if (entry.path.endswith(".jpg") or entry.path.endswith(".png")) and entry.is_file():
                output.append(str(entry.path))
                size += 1

        return output, size

    # args: paths: array of the paths of all the elements
    #        size: size of the database
    # return: array of the vectors of all the images in the database
    def _generateVectors(self, paths, size):
        output = np.ndarray(shape=(size, 768))
        i = 0

        for path in paths:
            output[i] = computeHistoVector(getImage((path)))
            i += 1
        
        return output

    def getVectors(self):
        return self.__vectors

    def getImagePaths(self):
        return self.__imagesPaths     

