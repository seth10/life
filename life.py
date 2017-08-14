import time, random
import curses, locale

def print2D(world):
    for i, row in enumerate(world):
        for j, element in enumerate(row):
            pad.addstr(i, j, u'\u25CB'.encode('utf-8') if element else " ")
    pad.refresh(0,0, 0,0, len(world), len(world[0]))

def make2DList(rows, columns, generator = lambda: False):
    return [[generator() for _ in range(rows)] for _ in range(columns)]

def iterate(today):
    tomorrow = make2DList(len(today), len(today[0]))
    for i, row in enumerate(tomorrow):
        for j, element in enumerate(row):
            neighbors = sum([ (x,y) != (0,0) and today[(i+x)%len(today)][(j+y)%len(row)] for x in [-1,0,1] for y in [-1,0,1] ])
            tomorrow[i][j] = (2 <= neighbors <= 3)
    return tomorrow

if __name__ == "__main__":
    SIZE = 7
    DELAY = 0.01
    MAX_ITERATIONS = 2*int(1/DELAY) # let the simulation run up to 2 seconds
    try:
        locale.setlocale(locale.LC_ALL, '')
        stdscr = curses.initscr()
        pad = curses.newpad(SIZE, SIZE+1)
        history = [make2DList(SIZE, SIZE, lambda: random.random() < 0.5)]
        while len(history) < MAX_ITERATIONS:
            history.append(iterate(history[-1]))
            print2D(history[-1])
            time.sleep(DELAY)
            if len(history) >= 3 and history[-1] == history[-3]: # TODO: search for longer stable patterns
                break
        if len(history) < MAX_ITERATIONS:
            resultMessage = "Stable after {} iterations".format(len(history))
        else:
            resultMessage = "Did not stabilize after {} iterations".format(MAX_ITERATIONS)
        pad.resize(SIZE+1, len(resultMessage)+1)
        pad.addstr(SIZE, 0, resultMessage)
        pad.refresh(SIZE,0, SIZE,0, SIZE,len(resultMessage))
        curses.flushinp() # discard any input received while simulation was running
        pad.getch() # wait for any keypress
    finally: # even if there were any exceptions, be sure curses stops so the prompt returns
        curses.endwin()
