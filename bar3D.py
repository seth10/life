import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm

data = [
    [0,  8, 19, 36, 37, 24, 16,  5, 1, 0, 0],
    [0, 15, 37, 37, 39, 33, 34,  8, 0, 0, 0],
    [0, 16, 30, 41, 37, 24, 27,  7, 0, 0, 0],
    [0, 28, 48, 50, 44, 40, 36, 14, 2, 0, 0],
    [0, 36, 61, 64, 65, 62, 53, 26, 0, 1, 0]
]

result = np.array(data, dtype=np.int)

fig = plt.figure(figsize=(6,5), dpi=150)
ax = fig.add_subplot(111, projection='3d')

xpos = np.arange(len(data[0]))
ypos = np.arange(len(data))

xposM, yposM = np.meshgrid(xpos, ypos, copy=False)
zpos = result.ravel()

x = xposM.ravel()
y = yposM.ravel()
z = zpos*0

dx = 0.5
dy = 0.5
dz = zpos

ax.w_xaxis.set_ticks(xpos + dx/2)
ax.w_xaxis.set_ticklabels(['0','10','20','30','40','50','60','70','80','90','100'])

ax.w_yaxis.set_ticks(ypos + dy/2)
ax.w_yaxis.set_ticklabels(['5x5', '6x6', '7x7', '8x8', '9x9'])

ax.set_title('Initial cell population and grid size vs stabilization/eradication')
ax.set_xlabel('Percentage of cells initially alive')
ax.set_ylabel('Grid size')
ax.set_zlabel('Percentage of simulations stabilized')

values = np.linspace(0.2, 1, x.shape[0])
colors = cm.rainbow(values)
ax.bar3d(x, y, z, dx, dy, dz, colors)
plt.show()
