from utils import *

class Query:
    __path = "" 
    __data = None
    __vector = None 

    def __init__(self, path):
        self.__path = path
        self.__data = getImage(self.__path)        
        self.__vector = computeHistoVector(self.__data)

    def getVector(self):
        return self.__vector

