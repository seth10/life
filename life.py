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
            livingNeighbors = 0 # TODO: use reduce
            for n,m in [(x,y) for x in [-1,0,1] for y in [-1,0,1]]:
                if (n,m) != (0,0): # don't count self
                    if today[(i+n)%len(today)][(j+m)%len(today)]: livingNeighbors += 1
            tomorrow[i][j] = 2 <= livingNeighbors <= 3
    return tomorrow

if __name__ == "__main__":
    SIZE = 7
    MAX_ITERATIONS = 100000
    DELAY = 0.2
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
                pad.addstr(0,0, "Stable")
                pad.refresh(0,0, 0,0, 1,6)
                time.sleep(1)
                curses.endwin()
                print "Stable after {} iterations".format(len(history))
                break
    finally:
        curses.endwin()
