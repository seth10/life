from Tkinter import *

root = Tk()
canvas = Canvas(root, width=200, height=200, bg="white")
canvas.pack()
canvas.create_rectangle(10, 20, 30, 40, fill="black", width=0)
root.mainloop()
