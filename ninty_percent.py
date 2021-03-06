import time, random
import multiprocessing, functools
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
    return any(sum(history[-1], [])) # False: eradication, True: stable

if __name__ == "__main__":
    startTime = time.time()
    START_PERCENT = 0.9
    TRIALS = 10000
    POOL = multiprocessing.Pool()
    data = []
    for SIZE in range(5, 10):
        results = POOL.map(functools.partial(simulate, SIZE, START_PERCENT), range(TRIALS))
        data.append(sum(results)/float(TRIALS))
        print "{0}x{0} grid with {1:.0f}% initially alive: {2}% stable".format(SIZE, START_PERCENT*100, data[-1]*100)
    print "Took {:.2f} seconds.".format(time.time() - startTime)
    plot.bar(range(len(data)), data)
    plot.xlabel('Grid size')
    plot.ylabel('Fraction of simulations stabilized')
    plot.title('Stabilization (not eradication) at 90% initial population')
    plot.xticks(range(len(data)))
    plot.gca().set_xticklabels(['{0}x{0}'.format(i) for i in range(5, 10)])
    plot.show()
