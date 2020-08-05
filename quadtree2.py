

class Point:
    def __init__(self, x, y, content):
        self.x = x
        self.y = y
        self.content = content

class Node: # Essentially the bounding area the quadtree will be built inside of
    def __init__(self, cx, cy, w, h):
        self.cx = cx
        self.cy = cy

        # North, south, east, west bounding boxes
        self.north = cy + h/2
        self.south = cy - h/2
        self.east = cx + w/2
        self.west = cx - w/2

    # contains method
    def contains(self, point):
        return self.west <= point.x < self.east and self.south <= point.y < self.north

    def draw(self, ax, color, linewidth):
        ax.plot([self.north, self.north, self.south, self.south, self.north],
                [self.west, self.east, self.east, self.west, self.west], c=color, linewidth=linewidth)

class QuadTree: # The tree. The node passed to it is the root node, and it has 4 children
    def __init__(self, rootnode, max_p):
        self.rootnode = rootnode
        self.max_p = max_p
        self.points = []
        self.is_divided = False

    def split(self):
        if self.is_divided:
            print("Error: Asking to split an already split node.")
            return False

        ne_node = Node(self.rootnode.cx + (self.rootnode.w/4), self.rootnode.cy + (self.rootnode.h/4),
                       self.rootnode.w/2, self.rootnode.h/2)
        self.ne = QuadTree(ne_node, self.max_p)

        nw_node = Node(self.rootnode.cx - (self.rootnode.w/4), self.rootnode.cy + (self.rootnode.h/4),
                       self.rootnode.w/2, self.rootnode.h/2)
        self.nw = QuadTree(nw_node, self.max_p)

        sw_node = Node(self.rootnode.cx - (self.rootnode.w/4), self.rootnode.cy - (self.rootnode.h/4),
                       self.rootnode.w/2, self.rootnode.h/2)
        self.sw = QuadTree(sw_node, self.max_p)

        se_node = Node(self.rootnode.cx + (self.rootnode.w/4), self.rootnode.cy - (self.rootnode.h/4),
                       self.rootnode.w/2, self.rootnode.h/2)
        self.se = QuadTree(se_node, self.max_p)

    def insert(self, point):

        # Checks if the point is contained in the quadrant
        if not self.rootnode.contains(point):
            return False

        # Base case (insert point)
        if len(self.points) < self.max_p:
            self.points.append(point)
            return True

        if not self.is_divided:
            self.split()

        return self.ne.insert(point) or self.nw.insert(point) or self.sw.insert(point) or self.se.insert(point)

    def draw(self, ax, color='k', linewidth=1):
        self.rootnode.draw(ax, color, linewidth)
        if self.is_divided:
            self.ne.draw(ax, color, linewidth)
            self.nw.draw(ax, color, linewidth)
            self.sw.draw(ax, color, linewidth)
            self.se.draw(ax, color, linewidth)