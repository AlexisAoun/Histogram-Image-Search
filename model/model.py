from query import Query
from database import Database

class Model:
    __query = None 
    __database = None
    __numberOfRes = 0

    def __init__(self, queryPath, databaseName, databasePath, savePath = ".", numberOfRes=4):
       self.__query = Query(queryPath)
       self.__database = Database(databaseName, databasePath, savePath)
       self.__numberOfRes = numberOfRes
    
    def getQuery(self):
        return self.__query

    def setQuery(self, newQueryPath):
       self.__query = Query(newQueryPath)

    def getNumberOfRes(self):
        return self.__numberOfRes

    def setNumberOfRes(self, newNumberOfRes):
        self.__numberOfRes = newNumberOfRes

    def getDatabase(self): 
        return self.__database

    def setDatabase(self, newDBName, newDBPath, newSavePath):
        self.__database = Database(newDBName, newDBPath, newSavePath)
