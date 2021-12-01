from view.gui import Gui

class MainController:
    __view = None
    __model = None

    def __init__(self):
        self.__view = Gui()  
# def selectFile(self):
#     self.__userQueryPath = askopenfilename()
#     self.__userQueryPath.configure(text=self.__userQueryPath)

#     tmp = ImageTk.PhotoImage(Image.open(self.__userQueryPath))
#     self.__queryLabel.configure(image=tmp)
#     self.__queryLabel.image = tmp

#     self.__queryImageRatio = tmp.width() / tmp.height()

#     self.__root.update()
#     resizeAllImages(self.__root.winfo_width())
