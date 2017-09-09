from __future__ import division
import math, random
import multiprocessing, functools
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plot

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

def simulate(size, startPercent, *args):
    history = [make2DList(size, size, lambda: random.random() < startPercent)]
    while history[-1] not in history[:-1]:
        history.append(iterate(history[-1]))
    iterationCount = len(history) - 1
    cycleLength = iterationCount - history[:-1].index(history[-1])
    return iterationCount - cycleLength

if __name__ == "__main__":
    GRID_SIZE = 8
    START_FRACTIONS = [n/10 for n in range(0,11)]
    data = [0]*len(START_FRACTIONS)
    total = 0
    canvas = plot.figure().canvas
    bars = plot.bar(range(len(START_FRACTIONS)), data, label='5x5 grid')
    plot.xlabel('Fraction of environment initially populated')
    plot.ylabel('Generations before eradication or stabilization')
    plot.title('Initial population vs generation count')
    plot.legend()
    plot.xticks(range(len(data)))
    plot.gca().set_xticklabels(START_FRACTIONS)
    plot.show(block=False)
    axis = plot.gca()
    while True:
        total += 1
        for i, START_PERCENT in enumerate(START_FRACTIONS):
            data[i] += simulate(GRID_SIZE, START_PERCENT)
        for i, bar in enumerate(bars):
            bar.set_height(data[i]/total)
        hmax = max([bar.get_height() for bar in bars])
        axis.set_ylim([0, math.ceil(hmax/5)*5 + 2])
        canvas.draw()
        canvas.flush_events()
