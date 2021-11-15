class View:
    __userNumRes = 0
    __userQueryPath = ""
    __userDbPath = ""
    __userDbName = ""
    __resToDisplay = None

    def getUserNumRes(self):
        return self.__userNumRes

    def setUserNumRes(self, newNumOfRes):
        self.__userNumRes = newNumOfRes

    def getUserQueryPath(self):
        return self.__userQueryPath

    def setUserQueryPath(self, newQueryPath):
        self.__userQueryPath = newQueryPath

    def getUserBbPath(self):
        return self.__userDbPath

    def setUserDbPath(self, newDbPath):
        self.__userDbPath = newDbPath

    def getUserDbName(self):
        return self.__userDbName

    def setUserDbName(self, newDbName):
        self.__userDbName = newDbName

    def getResToDisplay(self):
        return self.__resToDisplay

    def setResToDisplay(self, resToDisplay):
        self.__resToDisplay = resToDisplay
