import random

def  print2D(mainList):
    print "Printing world"
    for subList in mainList:
        #print subList
        print ["O" if element else " " for element in subList]

def iterate(today):
    tomorrow = [[False for _ in range(len(today[0]))] for _ in range(len(today))]
    for i,row in enumerate(tomorrow):
        for j,col in enumerate(row):
            livingNeighbors = 0
            for n,m in [(x,y) for x in [-1,0,1] for y in [-1,0,1]]:
                if (n,m) != (0,0): # don't count self
                    if today[(i+n)%len(today)][(j+m)%len(today)]: livingNeighbors += 1
            tomorrow[i][j] = 2 <= livingNeighbors <= 3
            #tomorrow[i][j] = livingNeighbors
    return tomorrow

if __name__ == "__main__":
    SIZE = 10
    world = [[random.random() < 0.5 for _ in range(SIZE)] for _ in range(SIZE)]
    print2D(world)
    world = iterate(world)
    print2D(world)
    world = iterate(world)
    print2D(world)
