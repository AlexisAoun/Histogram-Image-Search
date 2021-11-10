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
    
