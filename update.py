import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import random

def animated_barplot():
    x = [random.random() for _ in range(5)]
    rects = plt.bar(range(len(x)), x, align = 'center')
    for i in range(500):
        x = [random.random() for _ in range(5)]
        for rect, h in zip(rects, x):
            rect.set_height(h)
        fig.canvas.draw()
        fig.canvas.flush_events()

fig = plt.figure()
plt.show(block=False)
animated_barplot()
