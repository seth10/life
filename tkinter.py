import time, random
from Tkinter import Tk, Canvas
import tkMessageBox

import functools
# needed so the partial function has a __name__ when root.after calls it
# thanks to louistiao.me/posts/adding-__name__-and-__doc__-attributes-to-functoolspartial-objects/
def partial(func, *args, **kwargs):
    partial_func = functools.partial(func, *args, **kwargs)
    functools.update_wrapper(partial_func, func)
    return partial_func

def print2D(world):
    for item in canvas.find_all():
        canvas.delete(item)
    for i, row in enumerate(world):
        for j, element in enumerate(row):
            if element:
               canvas.create_rectangle(i*BLOCK_SIZE, j*BLOCK_SIZE, (i+1)*BLOCK_SIZE, (j+1)*BLOCK_SIZE, fill="black", width=0)

def statusLine(text):
    canvas.create_text(2, SIZE*BLOCK_SIZE, anchor="nw", text=text)

def make2DList(rows, columns, generator = lambda: False):
    return [[generator() for _ in range(rows)] for _ in range(columns)]

def iterate(today):
    tomorrow = make2DList(len(today), len(today[0]))
    for i, row in enumerate(tomorrow):
        for j, element in enumerate(row):
            neighbors = sum([ today[(i+x)%len(today)][(j+y)%len(row)] for x in [-1,0,1] for y in [-1,0,1] if (x,y) != (0,0) ])
            tomorrow[i][j] = (2 <= neighbors <= 3) if today[i][j] else (neighbors == 3)
            # The Rules
            # * For a space that is 'populated':
            #   - Each cell with one or no neighbors dies, as if by solitude.
            #   - Each cell with four or more neighbors dies, as if by overpopulation.
            #   - Each cell with two or three neighbors survives.
            # * For a space that is 'empty' or 'unpopulated'
            #   - Each cell with three neighbors becomes populated.
    return tomorrow

def step(history, delay=0.1):
    print2D(history[-1])
    statusLine("Generation {}".format(len(history)-1))
    history.append(iterate(history[-1]))
    if history[-1] not in history[:-1]:
        root.after(int(delay*1000), partial(step, history, delay))
    else:
        iterationCount = len(history) - 1
        cycleLength = iterationCount - history[:-1].index(history[-1])
        if cycleLength == 1 and not any(sum(history[-1], [])):
            result = "Eradication after {} generations.".format(iterationCount-cycleLength)
        else:
            result = "Stable after {} generations with a cycle of length {}.".format(iterationCount-cycleLength, cycleLength)
        tkMessageBox.showinfo("Simulation complete", result)
        root.destroy()


if __name__ == "__main__":
    SIZE = 8
    DELAY = 0.1
    BLOCK_SIZE = 20 # size of each block on the canvas
    HISTORY = [make2DList(SIZE, SIZE, lambda: random.random() < 0.5)]
    root = Tk()
    canvas = Canvas(root, width=SIZE*BLOCK_SIZE, height=SIZE*BLOCK_SIZE+12, bg="white")
    canvas.pack()
    root.after(10, partial(step, HISTORY, DELAY))
    root.mainloop()
