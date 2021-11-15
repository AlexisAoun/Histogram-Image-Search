from view import View

from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image


class Gui(View):
    pass
    # main window
    __root = None

    # window base dimension
    __winWidth = 1000
    __winHeight = 1000

    # Frames that compose the gui
    __mainFrame = None
    __resultsFrame = None
    __searchFrame = None
    __queryFrame = None

    # elements of the search frame
    __searchButton = None
    __selectButton = None
    __pathLabel = None

    # elements of results Frame
    __imageLabels = []

    __images = []
    __imageRatios = []

    # elements of query Frame
    __queryLabel = None
    __queryTitle = None

    def __init__(self, numberOfRes=4):
        self.__userNumRes = numberOfRes
        self.__root = Tk()
        self.__root.title("Histogram Image Search")
        self.__root.geometry(str(self.__winWidth) + "x" + str(self.__winHeight))
        self.__root.update()
        self.__root.minsize(width=800, height=800)

        # initiating and placing the frames
        self.__mainFrame = ttk.Frame(self.__root)
        self.__mainFrame.grid(column=0, row=0)

        self.__resultsFrame = ttk.Frame(self.__mainFrame)
        self.__resultsFrame.grid(column=0, row=1)

        self.__searchFrame = ttk.Frame(self.__mainFrame)
        self.__searchFrame.grid(column=0, row=0)

        self.__queryFrame = ttk.Frame(self.__mainFrame, padding=(0, 50, 0, 0))
        self.__queryFrame.grid(column=0, row=2)

        # iniating and placing elements in search frame
        self.__searchButton = ttk.Button(self.__searchFrame, text="Search")
        self.__searchButton.grid(column=0, row=1)

        self.__pathLabel = ttk.Label(self.__searchFrame, text="Request image path")
        self.__pathLabel.grid(column=2, row=0)

        self.__selectButton = ttk.Button(
            self.__searchFrame, text="Select Image", command=selectFile
        )
        self.__selectButton.grid(column=1, row=1)

        self.__resultTitle = ttk.Label(self.__searchFrame, text="Results : ")
        self.__resultTitle.grid(column=1, row=2)

        # initiating and placing elements in query frame
        self.__queryLabel = ttk.Label(self.__queryFrame, text="No Image Selected")
        self.__queryLabel.grid(column=0, row=1)

        self.__queryTitle = ttk.Label(self.__queryFrame, text="Query Image :")
        self.__queryTitle.grid(column=0, row=0)

        # initiating and placing elements in result frame
        self.__imageLabels[0] = ttk.Label(self.__resultsFrame, text="No results")

        for i in range(1, self.__userNumRes):
            tmp = ttk.Label(self.__resultsFrame)
            self.__imageLabels.append(tmp)
