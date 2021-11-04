from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

root = Tk()
root.title("Histogram Image Search")

mainframe = ttk.Frame(root).grid(column=0, row=0)
image = ImageTk.PhotoImage(Image.open("data/small/queries/96978713_775d66a18d.jpg"))
imageLabel = ttk.Label(mainframe, image = image).grid()


root.mainloop()
