from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

root = Tk()
root.title("Histogram Image Search")
root.geometry("800x800")


paths = [
    "data/small/queries/96978713_775d66a18d.jpg",
    "data/small/queries/3178371973_60c6b8f110.jpg",
    "data/small/queries/3074617663_2f2634081d.jpg",
    "data/small/queries/1924234308_c9ddcf206d.jpg",
]

mainframe = ttk.Frame(root)
resultsFrame = ttk.Frame(mainframe)
mainframe.grid(column=0, row=0)
resultsFrame.grid(column=0, row=1)

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
    data = Image.open(paths[index])
    dataResized = data.resize((width, height), Image.ANTIALIAS)
    imageResized = ImageTk.PhotoImage(dataResized)
    imageLabels[index].configure(image=imageResized)
    imageLabels[index].image = imageResized


def resizeAllImages():
    root.update()
    winWidth = root.winfo_width()
    for i in range(len(paths)):
        resizeImage(
            width=int(winWidth / 4), height=int((winWidth / 4) / imageRatios[i]), index=i
        )
    resultsFrame.configure(padding=((1/4*winWidth)/2,3,3,0))

resizeAllImages()

imageLabels[0].grid(column=2, row=1)
imageLabels[1].grid(column=1, row=2)
imageLabels[2].grid(column=2, row=2)
imageLabels[3].grid(column=3, row=2)

# TODO : Make image size responsive (by taking width and height of window and update size
# of images)

def resizeImageCallback():
    resizeImage(200, 200, 3)

button = ttk.Button(mainframe, text="resize", command=resizeImageCallback).grid(
    column=2, row=3
)

root.mainloop()
