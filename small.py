from __future__ import division
import random

def make2DList(rows, columns, generator = lambda: False):
    return [[generator() for _ in range(rows)] for _ in range(columns)]

def iterate(today):
    tomorrow = make2DList(len(today), len(today[0]))
    for i, row in enumerate(tomorrow):
        for j, element in enumerate(row):
            neighbors = sum([ today[(i+x)%len(today)][(j+y)%len(row)] for x in [-1,0,1] for y in [-1,0,1] if (x,y) != (0,0) ])
            tomorrow[i][j] = (2 <= neighbors <= 3) if today[i][j] else (neighbors == 3)
    return tomorrow

def simulate(size, startPercent):
    history = [make2DList(size, size, lambda: random.random() < startPercent)]
    while history[-1] not in history[:-1]:
        history.append(iterate(history[-1]))
    iterationCount = len(history) - 1
    cycleLength = iterationCount - history[:-1].index(history[-1])
    return iterationCount - cycleLength

if __name__ == "__main__":
    TRIALS = 1000
    for SIZE in range(5, 10):
        for START_PERCENT in [n/10.0 for n in range(0,11)]:
            results = [simulate(SIZE, START_PERCENT) for _ in range(TRIALS)]
            print "{0}x{0} grid with {1:3.0f}% initially alive: average {2:2.0f} generations".format(SIZE, START_PERCENT*100, round(sum(results)/len(results)))
