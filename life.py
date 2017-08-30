import random, multiprocessing, functools

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
    TRIALS = 100000
    for SIZE in range(5, 10):
        #for START_PERCENT in map(lambda n: n/10.0, range(1,10)):
            START_PERCENT = 0.9
            pool = multiprocessing.Pool(processes=4)
            results = pool.map(functools.partial(simulate, SIZE, START_PERCENT), range(TRIALS))
            print "{0}x{0} grid with {1:.0f}% initially alive: {2}% stable".format(SIZE, START_PERCENT*100, sum(results)*100.0/len(results))
