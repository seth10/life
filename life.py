from __future__ import division
import random
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
    START_PERCENT = 0.5
    data = [0]*5
    total = 0
    canvas = plot.figure().canvas
    bars = plot.bar(range(5), [1]*5)
    plot.xlabel('Grid size')
    plot.ylabel('Generations before eradication/stabilization')
    plot.title('Grid size vs iteration counts')
    plot.xticks(range(len(data)))
    plot.gca().set_xticklabels(['{0}x{0}'.format(i) for i in range(5, 10)])
    plot.show(block=False)
    axis = plot.gca()
    while True:
        total += 1
        for SIZE in range(5, 10):
            data[SIZE-5] += simulate(SIZE, START_PERCENT)
        for i, bar in enumerate(bars):
            bar.set_height(data[i]/total)
        axis.relim()
        axis.autoscale_view()
        canvas.draw()
        canvas.flush_events()
