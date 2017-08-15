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

def simulate(size, delay, maxIterations):
    history = [make2DList(size, size, lambda: random.random() < 0.5)]
    while len(history) < maxIterations:
        print2D(history[-1])
        time.sleep(delay)
        history.append(iterate(history[-1]))
        if history[-1] in history[:-1]:
            break
    if len(history) < maxIterations:
        iterationCount = len(history) - 1
        cycleLength = iterationCount - history[:-1].index(history[-1])
        return "Stable after {} iterations with a cycle of length {}.".format(iterationCount-cycleLength, cycleLength)
    else:
        return "Did not stabilize after {} iterations.".format(maxIterations)


if __name__ == "__main__":
    SIZE = 8
    DELAY = 0.1
    MAX_ITERATIONS = 10*int(1/DELAY) # let the simulation run up to 10 seconds
    try:
        locale.setlocale(locale.LC_ALL, '')
        stdscr = curses.initscr()
        curses.curs_set(0) # hide curosr
        ch = ord('\n') # pretend Enter was just pressed to run the simulation at least once
        while ch == ord('\n'):
            stdscr.clear()
            result = simulate(SIZE, DELAY, MAX_ITERATIONS)
            stdscr.addstr(SIZE, 0, result)
            stdscr.addstr(SIZE+1, 0, "Press Enter to run another simulation, or any other key to quit...")
            curses.flushinp() # discard any input received while simulation was running
            ch = stdscr.getch() # wait for any keypress
    finally: # even if there were any exceptions, be sure curses stops so the prompt returns
        curses.endwin()
