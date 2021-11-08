from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

root = Tk()
root.title("Histogram Image Search")

mainframe = ttk.Frame(root).grid(column=0, row=0)
imageTop = ImageTk.PhotoImage(Image.open("data/small/queries/96978713_775d66a18d.jpg"))
imageBot1 = ImageTk.PhotoImage(Image.open("data/small/queries/3178371973_60c6b8f110.jpg"))
imageBot2 = ImageTk.PhotoImage(Image.open("data/small/queries/3074617663_2f2634081d.jpg"))
imageBot3 = ImageTk.PhotoImage(Image.open("data/small/queries/1924234308_c9ddcf206d.jpg"))

# TODO : Make image size responsive (by taking width and height of window and update size
# of images)

imageLabel1 = ttk.Label(mainframe, image = imageTop)
imageLabel1.grid(column=2, row=1)
imageLabel2 = ttk.Label(mainframe, image = imageBot2).grid(column=2, row=2)
imageLabel3 = ttk.Label(mainframe, image = imageBot1).grid(column=1, row=2)
imageLabel4 = ttk.Label(mainframe, image = imageBot3).grid(column=3, row=2)


def resizeMainImage():
    data = Image.open("data/small/queries/96978713_775d66a18d.jpg")
    dataResized = data.resize((200, 200), Image.ANTIALIAS)
    imageResized = ImageTk.PhotoImage(dataResized)
    imageLabel1.configure(image=imageResized)
    imageLabel1.image = imageResized

button = ttk.Button(mainframe, text='resize', command = resizeMainImage).grid(column=2, row=3)

root.mainloop()

