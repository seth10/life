import time, random
import curses, locale

def print2D(world):
    for i, row in enumerate(world):
        for j, element in enumerate(row):
            stdscr.addstr(i, j, u'\u25CB'.encode('utf-8') if element else " ")
    stdscr.refresh()

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

if __name__ == "__main__":
    SIZE = 8
    DELAY = 0.1
    MAX_ITERATIONS = 10*int(1/DELAY) # let the simulation run up to 10 seconds
    try:
        locale.setlocale(locale.LC_ALL, '')
        stdscr = curses.initscr()
        history = [make2DList(SIZE, SIZE, lambda: random.random() < 0.5)]
        while len(history) < MAX_ITERATIONS:
            print2D(history[-1])
            time.sleep(DELAY)
            history.append(iterate(history[-1]))
            if history[-1] in history[:-1]:
                break
        if len(history) < MAX_ITERATIONS:
            iterationCount = len(history)-1
            cycleLength = iterationCount - history[:-1].index(history[-1])
            stdscr.addstr(SIZE, 0, "Stable after {} iterations with a cycle of length {}".format(iterationCount-cycleLength, cycleLength))
        else:
            stdscr.addstr(SIZE, 0, "Did not stabilize after {} iterations".format(MAX_ITERATIONS))
        curses.flushinp() # discard any input received while simulation was running
        stdscr.getch() # wait for any keypress
    finally: # even if there were any exceptions, be sure curses stops so the prompt returns
        curses.endwin()
