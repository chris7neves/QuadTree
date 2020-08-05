import numpy as np
import matplotlib.pyplot as plt
from quadtree import Point, Rectangle, Quadtree

DPI = 72
np.random.seed(60)

width, height = 600, 400

N = 500
coords = np.random.randn(N, 2) * height/3 + (width/2, height/2)
points = [Point(*coord) for coord in coords]
print(len(points))
center = Point(width/2, height/2)
domain = Rectangle(center, height, width)
qtree = Quadtree(domain, 5)
for point in points:
    qtree.insert(point)

print('Number of points in the domain =', len(qtree)) # it might not be adding all the points for some reason

fig = plt.figure(figsize=(700/DPI, 500/DPI), dpi=DPI)
ax = plt.subplot()
ax.set_xlim(0, width)
ax.set_ylim(0, height)
qtree.draw(ax)

ax.scatter([p.x for p in points], [p.y for p in points], s=4)
ax.set_xticks([])
ax.set_yticks([])


domain.draw(ax, color='r', linewidth=5)
ax.invert_yaxis()
plt.tight_layout()
plt.savefig('search-quadtree.png', DPI=72)
plt.show()