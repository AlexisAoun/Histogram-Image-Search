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

imageLabel = ttk.Label(mainframe, image = imageTop).grid(column=2, row=1)
imageLabel = ttk.Label(mainframe, image = imageBot1).grid(column=1, row=2)
imageLabel = ttk.Label(mainframe, image = imageBot2).grid(column=2, row=2)
imageLabel = ttk.Label(mainframe, image = imageBot3).grid(column=3, row=2)

root.mainloop()
