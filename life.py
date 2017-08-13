import random
import curses
import time

def print2D(world):
    for i, row in enumerate(world):
        for j, element in enumerate(row):
            pad.addch(i, j, "O" if element else " ")
    pad.refresh(0,0, 0,0, len(world), len(world[0]))

def iterate(today):
    tomorrow = [[False for _ in range(len(today[0]))] for _ in range(len(today))]
    for i,row in enumerate(tomorrow):
        for j,col in enumerate(row):
            livingNeighbors = 0
            for n,m in [(x,y) for x in [-1,0,1] for y in [-1,0,1]]:
                if (n,m) != (0,0): # don't count self
                    if today[(i+n)%len(today)][(j+m)%len(today)]: livingNeighbors += 1
            tomorrow[i][j] = 2 <= livingNeighbors <= 3
    return tomorrow

if __name__ == "__main__":
    try:
        SIZE = 10
        stdscr = curses.initscr()
        pad = curses.newpad(SIZE, SIZE+1)
        world = [[random.random() < 0.5 for _ in range(SIZE)] for _ in range(SIZE)]
        for _ in range(10):
            world = iterate(world)
            print2D(world)
            time.sleep(0.5)
    finally:
        curses.endwin()
