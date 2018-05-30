import utils


"""
:param[opt] bool cacheNodeAtRuntime When __true__, returns an empty `grid` instance, so that
    later on, indexing a non-cached `node` will cause it to be created and cache within the `grid` on purpose (i.e, when needed).
        This is a __memory-safe__ option, in case your dealing with some tight memory constraints.
        Defaults to __false__ when omitted."""

class Grid:
    straight_offsets = [
        {'x': 1, 'y': 0}, # [[W]]
        {'x': -1,'y': 0}, # [[E]]
        {'x': 0, 'y': 1}, # [[S]]
        {'x': 0, 'y': -1} # [[N]]
    ]

    diagonal_offsets = [
        {'x': -1, 'y': -1}, # [[NW]],
        {'x': 1, 'y': -1}, # [[NE]]
        {'x': -1, 'y': 1}, # [[SW]],
        {'x': 1, 'y': 1} # [[SE]]
    ]

    def __init__(self, map):
        """
        Inits a new `grid`

        :param table|string map A collision map - (2D array) with consecutive indices (starting at 0 or 1)
        or a `string` with line-break chars (<code>\n</code> or <code>\r</code>) as row delimiters.

        @usage
        -- A simple 3x3 grid
        local myGrid = Grid:new({{0,0,0},{0,0,0},{0,0,0}})

        -- A memory-safe 3x3 grid

        :param map:
        :param walkable:
        """
        self.map = map
        self.is_annotated = {}
        self.nodes, self.min_x, self.max_x, self.min_y, self.max_y = utils.array_to_nodes(map)
        self.width = self.max_x - self.min_x
        self.height = self.max_y - self.min_y

    def is_walkable(self, x, y, walkable=None, clearance=None):
        if x < 0 or y < 0:
            return False
        try:
            node_value = self.map[y][x]
        except IndexError:
            return False

        if walkable is None:
            return True

        has_enough_clearance = True

        if clearance:
            if not self.is_annotated.get(walkable):
                return False

            node = self.get_node_at(x, y)

            # In this context, a walkable is representing the entity
            # that is trying to get clearance through the node
            node_clearance = node.get_clearance(walkable)
            has_enough_clearance = node_clearance >= clearance

        try:
            return walkable(node_value) and has_enough_clearance
        except TypeError:
            return node_value == walkable and has_enough_clearance

    def get_node_at(self, x, y):
        if x < 0 or y < 0:
            return None
        try:
            return self.nodes[y][x]
        except IndexError:
            return None

    def imap(self, f, *args, **kwargs):
        for i, node in enumerate(self.nodes):
            self.nodes[i] = f(node, *args, **kwargs)

    def get_neighbours(self, node, walkable, allow_diagonal=False, tunnel=False, clearance=False):
        """
          --- Returns neighbours. The returned value is an array of __walkable__ nodes neighbouring a given `node`.     @class function
        @tparam node node a given `node`
        @tparam[opt] string|int|func walkable the value for walkable locations in the collision map array (see @{Grid:new}).
        Defaults to __false__ when omitted.
        @tparam[optchain] bool allowDiagonal when __true__, allows adjacent nodes are included (8-neighbours).
        Defaults to __false__ when omitted.
        @tparam[optchain] bool tunnel When __true__, allows the `pathfinder` to tunnel through walls when heading diagonally.
        @tparam[optchain] int clearance When given, will prune for the neighbours set all nodes having a clearance value lower than the passed-in value
        Defaults to __false__ when omitted.
        @treturn {node,...} an array of nodes neighbouring a given node
        @usage
        local aNode = myGrid:getNodeAt(5,6)
        local neighbours = myGrid:getNeighbours(aNode, 0, true)
           :param node:
        :param walkable:
        :param allow_diagonal:
        :param tunnel:
        :param clearance:
        :return:
        """
        neighbours = []
        for straightOffset in self.straight_offsets:
            n = self.get_node_at(node.x + straightOffset['x'], node.y + straightOffset['y'])
            if n and self.is_walkable(n.x, n.y, walkable, clearance):
                neighbours.append(n)

        if not allow_diagonal:
            return neighbours

        for diagonal_offset in self.diagonal_offsets:
            n = self.get_node_at(node.x + diagonal_offset['x'], node.y + diagonal_offset['y'])
            if n and self.is_walkable(n.x, n.y, walkable, clearance):
                if tunnel:
                    neighbours.append(n)
                else:
                    n1 = self.get_node_at(node.x + diagonal_offset['x'], node.y)
                    n2 = self.get_node_at(node.x, node.y + diagonal_offset['y'])
                    if n1 and n2 and not self.is_walkable(n1.x, n1.y, walkable, clearance) and not self.is_walkable(n2.x, n2.y, walkable, clearance):
                        pass
                    else:
                        neighbours.append(n)

        return neighbours


class PostProcessGrid(Grid):
    """
    Use this when dealing with low-memory constraints, since the nodes will be
     created on the fly as they are going to be used or accessed
    """
    def __init__(self, map, walkable):
        super().__init__(map, walkable)
        self.nodes = []
        self.min_x, self.max_x, self.min_y, self.max_y = utils.get_array_bounds(map)
        self.width = self.max_x - self.min_x + 1
        self.height = self.max_y - self.min_y + 1


class PreProcessGrid(Grid):
    """
    The default grid choice
    """
    def __init__(self, map, walkable):
        super().__init__(map, walkable)
        self.nodes, self.min_x, self.max_x, self.min_y, self.max_y = utils.array_to_nodes(map)
        self.width = self.max_x - self.min_x + 1
        self.height = self.max_y - self.min_y + 1
