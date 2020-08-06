

class Point:
    def __init__(self, x, y, content=None):
        self.x = x
        self.y = y
        self.content = content

    def __repr__(self):
        return f"{self.x}, {self.y}, {self.content}"

class Node: # Essentially the bounding area the quadtree will be built inside of
    def __init__(self, cx, cy, w, h):
        self.cx = cx
        self.cy = cy
        self.w = w
        self.h = h

        # North, south, east, west bounding boxes
        self.north = self.cy + h/2
        self.south = self.cy - h/2
        self.east = self.cx + w/2
        self.west = self.cx - w/2

    # contains method
    def contains(self, point):
        return self.west <= point.x < self.east and self.south <= point.y < self.north

    def draw(self, ax, color, linewidth):
        ax.scatter(self.cx, self.cy, c='r', s=3)
        ax.plot([self.west, self.east, self.east, self.west, self.west],
                [self.north, self.north, self.south, self.south, self.north], c=color, linewidth=linewidth)


class QuadTree: # The tree. The node passed to it is the root node, and it has 4 children
    def __init__(self, rootnode, max_p, depth=0):
        self.rootnode = rootnode
        self.max_p = max_p
        self.points = []
        self.is_divided = False
        self.depth = depth
        self.ne = None
        self.nw = None
        self.sw = None
        self.se = None

    def split(self):
        if self.is_divided:
            print("Error: Asking to split an already split node.")
            return False

        ne_node = Node(self.rootnode.cx + (self.rootnode.w/4), self.rootnode.cy + (self.rootnode.h/4),
                       self.rootnode.w/2, self.rootnode.h/2)
        self.ne = QuadTree(ne_node, self.max_p, self.depth+1)

        nw_node = Node(self.rootnode.cx - (self.rootnode.w/4), self.rootnode.cy + (self.rootnode.h/4),
                       self.rootnode.w/2, self.rootnode.h/2)
        self.nw = QuadTree(nw_node, self.max_p, self.depth+1)

        sw_node = Node(self.rootnode.cx - (self.rootnode.w/4), self.rootnode.cy - (self.rootnode.h/4),
                       self.rootnode.w/2, self.rootnode.h/2)
        self.sw = QuadTree(sw_node, self.max_p, self.depth+1)

        se_node = Node(self.rootnode.cx + (self.rootnode.w/4), self.rootnode.cy - (self.rootnode.h/4),
                       self.rootnode.w/2, self.rootnode.h/2)
        self.se = QuadTree(se_node, self.max_p, self.depth+1)

        self.is_divided = True

        # self.reorganize1()
        # for point in self.points:
        #     self.reorganize(point)
        # self.points.clear()
        temp = self.points.copy()
        self.points.clear()
        for point in temp:
            self.insert(point)
        temp.clear()

    def reorganize1(self):
        for point in self.points:
            if self.ne.rootnode.contains(point):
                self.ne.points.append(point)
            elif self.nw.rootnode.contains(point):
                self.nw.points.append(point)
            elif self.sw.rootnode.contains(point):
                self.sw.points.append(point)
            elif self.se.rootnode.contains(point):
                self.se.points.append(point)
        self.points.clear()

    def reorganize(self, point):
        return self.ne.insert(point) or self.nw.insert(point) or self.sw.insert(point) or self.se.insert(point)

    def insert(self, point):

        # Checks if the point is contained in the quadrant. Ignored for root
        if not self.rootnode.contains(point):
            return False

        if self.is_divided: # THIS WAS THE MISSING LINE AHHHHHHH FINALLY... still causes recursion issues when max p is 1 though
            return self.ne.insert(point) or self.nw.insert(point) or self.sw.insert(point) or self.se.insert(point)

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