import matplotlib.pyplot as plot

data = [0.00, 0.36, 0.61, 0.64, 0.65, 0.62, 0.53, 0.26, 0.00, 0.01, 0.00]
labels = map(lambda n: n/10.0, range(0, len(data)))

plot.bar(range(len(data)), data)

plot.xlabel('Fraction of cells initially alive')
plot.ylabel('Fraction of simulations stabilized')
plot.title('Initial cell population vs stabilization/eradication')
plot.xticks(range(len(data)))
plot.gca().set_xticklabels(labels)

plot.show()
