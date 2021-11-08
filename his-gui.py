from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image

root = Tk()
root.title("Histogram Image Search")
root.geometry("1000x1000")

root.update()
winWidth = root.winfo_width()

queryPath = None
queryImageRatio = None
paths = [
    "data/small/queries/96978713_775d66a18d.jpg",
    "data/small/queries/3178371973_60c6b8f110.jpg",
    "data/small/queries/3074617663_2f2634081d.jpg",
    "data/small/queries/1924234308_c9ddcf206d.jpg",
]

def selectFile():
    global queryPath
    global queryImageRatio
    queryPath = askopenfilename()
    pathLabel.configure(text=queryPath)
    queryImage = ImageTk.PhotoImage(Image.open(queryPath))
    queryLabel.configure(image=queryImage)
    queryLabel.image = queryImage
    queryImageRatio = queryImage.width()/queryImage.height() 
    root.update()
    resizeAllImages(root.winfo_width())

mainframe = ttk.Frame(root)
resultsFrame = ttk.Frame(mainframe)
searchFrame = ttk.Frame(mainframe)
queryFrame = ttk.Frame(mainframe, padding=(0,100,0,0))

mainframe.grid(column=0, row=0)
resultsFrame.grid(column=0, row=1)
searchFrame.grid(column=0, row=0)
queryFrame.grid(column=0, row=2)

searchButton = ttk.Button(searchFrame, text="Search")
searchButton.grid(column=0, row=0)

pathLabel = ttk.Label(searchFrame, text="Request image path")
pathLabel.grid(column=2, row=0)

selectButton = ttk.Button(searchFrame, text="Select Image", command=selectFile)
selectButton.grid(column=1, row=0)

resultTitle = ttk.Label(searchFrame, text="Results : ")
resultTitle.grid(column=1, row=1)

queryLabel = ttk.Label(queryFrame, text="No Image Selected")
queryLabel.grid(column=0, row=1)

queryTitle = ttk.Label(queryFrame, text="Query Image :")
queryTitle.grid(column=0, row=0)

images = []
imageLabels = []
imageRatios = []

for path in paths:
    image = ImageTk.PhotoImage(Image.open(path))
    imageLabel = ttk.Label(resultsFrame, image=image)
    imageRatio = image.width() / image.height()

    images.append(image)
    imageLabels.append(imageLabel)
    imageRatios.append(imageRatio)

def resizeImage(width, height, index):
    if index == -1:
        data = Image.open(queryPath)
        dataResized = data.resize((width, height), Image.ANTIALIAS)
        imageResized = ImageTk.PhotoImage(dataResized)
        queryLabel.configure(image=imageResized)
        queryLabel.image = imageResized
    else :
        data = Image.open(paths[index])
        dataResized = data.resize((width, height), Image.ANTIALIAS)
        imageResized = ImageTk.PhotoImage(dataResized)
        imageLabels[index].configure(image=imageResized)
        imageLabels[index].image = imageResized


def resizeAllImages(width):
    print(queryPath)
    if queryPath is not None:
        resizeImage(
            width=int(width / 4), height=int((width / 4) / queryImageRatio), index=-1
        )
    for i in range(len(paths)):
        resizeImage(
            width=int(width / 4), height=int((width / 4) / imageRatios[i]), index=i
        )
    resultsFrame.configure(padding=((1/4*width)/2,3,3,0))

resizeAllImages(winWidth)

imageLabels[0].grid(column=2, row=1)
imageLabels[1].grid(column=1, row=2)
imageLabels[2].grid(column=2, row=2)
imageLabels[3].grid(column=3, row=2)

def windowChangeCallback(self):
    root.update()
    if winWidth != root.winfo_width():
        resizeAllImages(root.winfo_width())

root.bind('<Configure>', windowChangeCallback)

root.mainloop()
