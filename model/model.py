from query import Query
from database import Database
from distance import *
from lsh import LSH


class Model:
    __query = None
    __database = None
    __numberOfRes = 0

    def __init__(
        self, queryPath, databaseName, databasePath, savePath=".", numberOfRes=4
    ):
        self.__query = Query(queryPath)
        self.__database = Database(databaseName, databasePath, savePath)
        self.__numberOfRes = numberOfRes

    # args: type of search : 0 - Most accurate search by brute force, slowest search not suitable on large data set
    #                        1 - Quicker search with an accuracy of 80%, using LSH and all the dimensions, with a
    #                            set of tested and fixed parameters
    # return: Search results : tuple of indexes of the results and the respective distances to query
    #         returns number of solutions if search 1 is chosen
    def search(self, typeOfSearch=0):
        res = -1

        if typeOfSearch == 0:
            res = self._bruteSearch()
        elif typeOfSearch == 1:
            res = self._optimalLshSearch()

        return res

    # return: the indexes and the distances of the result of a brute search using Euclidien distance
    #         -1 if database and/or query is not set
    def _bruteSearch(self):
        if self.__database is not None and self.__query is not None:
            return knn_search(
                self.__database.getVectors(),
                self.__query.getVector(),
                self.__numberOfRes,
            )
        else:
            return -1

    # return: the indexes and the distances of the result of an optimal lsh search with an accuracy of 80%
    #         -1 if database and/or query is not set
    def _optimalLshSearch(self):
        if self.__database is not None and self.__query is not None:
            w = 0.065
            nbProjections = 6
            nbTabHash = 3

            lsh = LSH(nb_projections=nbProjections, nb_tables=nbTabHash, w=w)
            lsh.fit(self.__database.getVectors())
            return lsh.kneighbors(self.__query.getVector())
        else:
            return -1

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
