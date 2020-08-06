import matplotlib.pyplot as plt
import numpy as np
from quadtree2 import *
import time


np.random.seed(109)

fig = plt.figure()
ax = fig.add_subplot(111)

# def onclick(event):
#     print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
#           (event.button, event.x, event.y, event.xdata, event.ydata))
#     plt.plot(event.xdata, event.ydata, ',')
#     fig.canvas.draw()


# Concentrated points
x_values = np.random.randint(340, 350, 20)
y_values = np.random.randint(340, 350, 20)

# Distributed
# x_values = np.random.randint(0, 700, 200)
# y_values = np.random.randint(0, 700, 200)

# Single points
# x_values = [0, 5, 350]
# y_values = [0, 5, 350]

point_coords = np.concatenate((np.expand_dims(x_values, axis=1), np.expand_dims(y_values, axis=1)), axis=1)

point_list = [Point(x, y) for x, y in point_coords]

ax.scatter(x_values, y_values, c='b', s=1)

point_limit = 1
quadtree2 = QuadTree(Node(350, 350, 700, 700), point_limit)
for point in point_list:
    quadtree2.insert(point)




quadtree2.draw(ax, linewidth=0.5)

# cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()