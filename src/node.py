class Node:
    """
    The `node` represents a cell (or a tile) on a collision map. Basically, for each single cell (tile)
    in the collision map passed-in upon initialization, a `node` object will be generated
    and then cached within the `grid`.

    In the following implementation, nodes can be compared using the `<` operator. The comparison is
    made with regards of their `f` cost. From a given node being examined, the `pathfinder` will expand the search
    to the next neighbouring node having the lowest `f` cost. Heaps make use of __lt__ to sort their contents.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = None
        self.h = None
        self.opened = False
        self.closed = False
        self.parent = None
        self.clearance = {}

    @property
    def f(self):
        return self.g + self.h

    @property
    def position(self):
        return self.x, self.y

    def close(self):
        self.closed = True

    def open(self):
        self.opened = True

    def get_clearance(self, walkable):
        """
        Returns the amount of true [clearance](http://aigamedev.com/open/tutorial/clearance-based-pathfinding/#TheTrueClearanceMetric)
        for a given `node`
        :param string|int|func walkable: the value for walkable locations in the collision map array.
        :return: int the clearance of the `node`
        """
        return self.clearance.get(walkable)

    def remove_clearance(self, walkable):
        self.clearance[walkable] = None

    def reset(self):
        self.g = None
        self.h = None
        self.opened = False
        self.closed = False
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f

    def __repr__(self):
        return f'({self.x}, {self.y})'
