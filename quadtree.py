# Most of sourcecode taken from https://scipython.com/blog/quadtrees-2-implementation-in-python/ to be used in boids simulation

import numpy as np

class Point:
    def __init__(self, x, y, content=None):
        """ Content is used to link the point to another datatype or object, which would be found at the point."""
        self.x = x
        self.y = y
        self.content = content


class Rectangle:
    def __init__(self, point, h, w):
        """ Point is the center of the rectangle."""
        self.point = point
        self.w = w
        self.h = h
        self.east, self.west = point.x + (w/2), point.x - (w/2)
        self.north, self.south = point.y + (h/2), point.y - (h/2)
        self.center_x = point.x
        self.center_y = point.y

    def contains(self, point):
        """ Checks to see if a point is within the rectangle's bounds."""
        return self.east >= point.x > self.west and self.north >= point.y > self.south

    def intersects(self, rect):
        """ Checks for conditions that when true, mean that 2 rectangles don't overlap."""
        return not (self.east < rect.west or
                    self.north < rect.south or
                    self.west > rect.east or
                    self.south > rect.north)

    def contains(self, point):
        """ Determines if a point is located inside the rectangle (positionally only)."""
        try: # Assigns it to the point x and y attributes. If point is passed as a tuple instead, unpack the tuple.
            x, y = point.x, point.y
        except AttributeError:
            x, y = point

        return self.west <= x <= self.east and self.north >= y >= self.south

    def draw(self, ax, linewidth=1, color='k'):
        l_x, l_y = self.west, self.north
        r_x, r_y = self.east, self.south
        ax.plot([l_x, r_x, r_x, l_x], [l_y, l_y, r_y, r_y], linewidth=linewidth, color=color)



class Quadtree:
    def __init__(self, boundary, point_limit, depth=0):
        self.boundary = boundary
        self.point_limit = point_limit
        self.points = []
        self.node_depth = depth
        self.divided = False
        self.ne, self. nw, self.sw, self.se = None

    def split(self):
        center_x, center_y = self.boundary.center_x, self.boundary.center_y # The center of a provided boundary
        w, h = self.boundary.w/2, self.boundary.h/2 # The width and height of a quadrant of a provided boundary

        ne_rect = Rectangle(Point(center_x + w/2, center_y + h/2), h, w)
        self.ne = Quadtree(ne_rect, self.point_limit, self.node_depth + 1)

        nw_rect = Rectangle(Point(center_x - w/2, center_y + w/2), h, w)
        self.nw = Quadtree(nw_rect, self.point_limit, self.node_depth + 1)

        sw_rect = Rectangle(Point(center_x - w/2, center_y - w/2), h, w)
        self.sw = Quadtree(sw_rect, self.point_limit, self.node_depth + 1)

        se_rect = Rectangle(Point(center_x + w/2, center_y - w/2), h, w)
        self.se = Quadtree(se_rect, self.point_limit, self.node_depth + 1)

        self.divided = True

    def insert(self, point):


    def draw(self, ax, linewidth=1, color='k'):
        self.boundary.draw(ax, linewidth, color)
        if self.divided:
            self.ne.draw(ax, linewidth, color)
            self.nw.draw(ax, linewidth, color)
            self.sw.draw(ax, linewidth, color)
            self.se.draw(ax, linewidth, color)


