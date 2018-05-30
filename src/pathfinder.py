import utils
from heuristics import manhattan
from search import astar


class Pathfinder:
    def __init__(self, grid, finder, walkable, **kwargs):
        self.grid = grid
        self.finder = finder or astar.search
        self.walkable = walkable  # can be a string, a number or a function
        self.tunneling = kwargs.get('tunneling', False)
        self.heuristic = kwargs.get('heuristic') or manhattan
        self.allow_diagonal = True
        self.to_clear = {}

    def annotate_grid(self):
        """
        Evaluates [clearance](http://aigamedev.com/open/tutorial/clearance-based-pathfinding/#TheTrueClearanceMetric)
        for the whole `grid`. It should be called only once, unless the collision map or the
        __walkable__ attribute changes. The clearance values are calculated and cached within the grid nodes.

        :return pathfinder: (the calling `pathfinder` itself, can be chained)
        """
        for y in range(self.grid.max_y - 1, self.grid.min_y - 1, -1):
            for x in range(self.grid.max_x - 1, self.grid.min_x - 1, -1):
                node = self.grid.get_node_at(x, y)
                if self.grid.is_walkable(x, y, self.walkable):
                    nr = self.grid.get_node_at(node.x + 1, node.y)
                    nrd = self.grid.get_node_at(node.x + 1, node.y + 1)
                    nd = self.grid.get_node_at(node.x, node.y + 1)
                    if nr and nrd and nd:
                        m = nrd.clearance[self.walkable] or 0
                        m = (nd.clearance[self.walkable] or 0) < m and (nd.clearance[self.walkable] or 0) or m
                        m = (nr.clearance[self.walkable] or 0) < m and (nr.clearance[self.walkable] or 0) or m
                        node.clearance[self.walkable] = m + 1
                    else:
                        node.clearance[self.walkable] = 1
                else:
                    node.clearance[self.walkable] = 0
        self.grid.is_annotated[self.walkable] = True
        return self

    def get_path(self, start_x, start_y, end_x, end_y, clearance=1):
        """
        Calculates a `path`. Returns the `path` from location __[startX, startY]__ to location __[endX, endY]__.
        Both locations must exist on the collision map. The starting location can be unwalkable.
        :param int start_x: the x-coordinate for the starting location
        :param int start_y: the y-coordinate for the starting location
        :param int end_x: the x-coordinate for the goal location
        :param int end_y: the y-coordinate for the goal location
        :param int clearance: the amount of clearance (i.e the pathing agent size) to consider
        :return path: a path (array of nodes) when found, otherwise None
        """
        self.reset()
        start_node = self.grid.get_node_at(start_x, start_y)
        end_node = self.grid.get_node_at(end_x, end_y)

        _end_node = self.finder(self, start_node, end_node, clearance, self.to_clear)
        if _end_node:
            return utils.trace_back_path(self, _end_node, start_node)

    def reset(self):
        for _, node in self.to_clear.items():
            node.reset()
        self.to_clear = {}

    def get_clearance_grid(self, walkable):
        output = []
        for y in range(self.grid.height):
            row = []
            for x in range(self.grid.width):
                node = self.grid.get_node_at(x, y)
                row.append(node.get_clearance(walkable))
            output.append(row)

        return output
