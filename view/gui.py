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

    __userNumRes = 0
    __resToDisplay = None
    __maxNumOfRes = 6
    __numOfRows = 0
    __numOfColumns = 0

    # elements of query Frame
    __queryLabel = None
    __queryTitle = None
    __queryImageRatio = 0
    __queryPath = None

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

        self.__imageLabels[0].grid(column=2, row=1)
        self.__imageLabels[1].grid(column=1, row=2)
        self.__imageLabels[2].grid(column=2, row=2)
        self.__imageLabels[3].grid(column=3, row=2)


    def _resizeImage(self, width, height, index):
        if index == -1:
            data = Image.open(self.__userQueryPath)
            dataResized = data.resize((width, height), Image.ANTIALIAS)
            imageResized = ImageTk.PhotoImage(dataResized)
            self.__queryLabel.configure(image=imageResized)
            self.__queryLabel.image = imageResized
        else:
            data = Image.open(self.__resToDisplay[index])
            dataResized = data.resize((width, height), Image.ANTIALIAS)
            imageResized = ImageTk.PhotoImage(dataResized)
            self.__imageLabels[index].configure(image=imageResized)
            self.__imageLabels[index].image = imageResized

    #TODO adapt this function to the new refactor, !!! replace userDBPath by resToDisplay
    def resizeAllImages(self):
        if self.__resToDisplay is not None:
            if self.__userQueryPath is not None:
                self._resizeImage(
                    width=int(self.__winWidth / 6),
                    height=int((self.__winWidth / 6) / self.__queryImageRatio),
                    index=-1,
                )
            for i in range(len(self.__resToDisplay)):
                self._resizeImage(
                    width=int(self.__winWidth / 4), 
                    height=int((self.__winWidth / 4) / self.__imageRatios[i]), 
                    index=i
                )
        self.__resultsFrame.configure(padding=((1 / 4 * self.__winWidth) / 2, 3, 3, 0))

    def displayResults(self, res, numOfRes):
        #if there's results displayed destroy all the results widgets
        if self.__resToDisplay is not None:
            for i in range(self.__userNumRes):
                self.__imageLabels[i].destroy() 


        self.__userNumRes = numOfRes
        self.__resToDisplay = res

        self.__numOfRows = 1 if self.__userNumRes < 3 else 2
        self.__numOfColumns = 1 if self.__userNumRes == 1 else 2 if self.__userNumRes < 5 else 3
         
        r = 0
        c = 0
        for i in range(self.__userNumRes):
            tmp = ImageTk.PhotoImage(Image.open(self.__resToDisplay[i]))
            self.__imageLables[i] = ttk.Label(self.__resultsFrame, image=tmp)
            self.__imageRatios[i] = tmp.width() / tmp.height()

            self.__imageLabels[i].grid(column=c, row=r)

            if c < self.__numOfColumns:
                c += 1 
            else:
                c = 0
                if r < self.__numOfRows:
                    r += 1 

    def selectFile(self):
        self.__queryPath = askopenfilename()
        self.__queryLabel.configure(text=self.__queryPath)

        tmp = ImageTk.PhotoImage(Image.open(self.__queryPath))
        self.__queryLabel.configure(image=tmp)
        self.__queryLabel.image = tmp

        self.__queryImageRatio = tmp.width() / tmp.height()

        self.__root.update()
        resizeAllImages(self.__root.winfo_width())
