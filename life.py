from __future__ import division
import time, random
import multiprocessing, functools
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

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
    POOL = multiprocessing.Pool()
    TRIALS = 100
    GRID_SIZES = range(5, 10)
    POPULATION_PERCENTAGES = map(lambda n: n/10, range(0,11))
    data = []
    for SIZE in GRID_SIZES:
        data.append([])
        for START_PERCENT in POPULATION_PERCENTAGES:
            results = POOL.map(functools.partial(simulate, SIZE, START_PERCENT), range(TRIALS))
            data[-1].append(sum(results)/TRIALS)
            print "{0}x{0} grid with {1:.0f}% initially alive: {2}% stable".format(SIZE, START_PERCENT*100, data[-1][-1]*100)

    print "Took {:.2f} seconds.".format(time.time() - startTime)

    fig = plt.figure(figsize=(8,5))
    ax = fig.gca(projection='3d')

    x = range(len(data[0])) * len(data)
    y = sum([[i]*len(data[0]) for i in range(len(data))], [])
    z = [0] * len(data[0]) * len(data)

    dx = 0.5
    dy = 0.5
    dz = sum(data, [])

    ax.w_xaxis.set_ticks([i+dx/2 for i in range(len(data[0]))])
    ax.w_xaxis.set_ticklabels(POPULATION_PERCENTAGES)

    ax.w_yaxis.set_ticks([i+dy/2 for i in range(len(data))])
    ax.w_yaxis.set_ticklabels(['{0}x{0}'.format(i) for i in GRID_SIZES])

    ax.set_title('Initial cell population and grid size vs stabilization/eradication')
    ax.set_xlabel('Fraction of cells initially alive')
    ax.set_ylabel('Grid size')
    ax.set_zlabel('Fraction of simulations stabilized')

    colors = cm.rainbow( [0.2 + (1-0.2)/(len(x)-1)*i for i in range(len(x))] )
    ax.bar3d(x, y, z, dx, dy, dz, colors)
    plt.tight_layout()
    plt.show()
