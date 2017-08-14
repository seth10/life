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
    for i,row in enumerate(tomorrow):
        for j,col in enumerate(row):
            livingNeighbors = 0
            for n,m in [(x,y) for x in [-1,0,1] for y in [-1,0,1]]:
                if (n,m) != (0,0): # don't count self
                    if today[(i+n)%len(today)][(j+m)%len(today)]: livingNeighbors += 1
            tomorrow[i][j] = 2 <= livingNeighbors <= 3
    return tomorrow

if __name__ == "__main__":
    SIZE = 10
    ITERATIONS = 20
    DELAY = 0.5
    try:
        locale.setlocale(locale.LC_ALL, '')
        stdscr = curses.initscr()
        pad = curses.newpad(SIZE, SIZE+1)
        world = make2DList(SIZE, SIZE, lambda: random.random() < 0.5)
        for _ in range(ITERATIONS):
            world = iterate(world)
            print2D(world)
            time.sleep(DELAY)
    finally:
        curses.endwin()
