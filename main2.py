import matplotlib.pyplot as plt
import numpy as np
from quadtree2 import *

np.random.seed(10)

fig = plt.figure()
ax = fig.add_subplot(111)

x_values = np.random.randint(0, 700, 200)
y_values = np.random.randint(0, 700, 200)

point_coords = np.concatenate((np.expand_dims(x_values, axis=1), np.expand_dims(y_values, axis=1)), axis=1)

ax.scatter(x_values, y_values, c='b', s=1)



plt.show()