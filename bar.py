import numpy as np
import matplotlib.pyplot as plot

data = [0.00, 0.36, 0.61, 0.64, 0.65, 0.62, 0.53, 0.26, 0.00, 0.01, 0.00]
labels = map(lambda n: n/10.0, range(0,11))

figure, axis = plot.subplots()
series = axis.bar(range(len(data)), data)

axis.set_xlabel('Fraction of cells initially alive')
axis.set_ylabel('Fraction of simulations stabilized')
axis.set_title('Initial cell population vs stabilization/eradication')
axis.set_xticks(range(len(data)))
axis.set_xticklabels(labels)

plot.show()
