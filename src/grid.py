from functools import partial
from typing import Dict, Optional, List, Any, Protocol

import utils
from node import Node
from mytypes.mytypes import Map
from mytypes.walkable import Walkable


class NodeMapper(Protocol):
    def __call__(self, node: Node, *args: Any, **kwargs: Any) -> Node:
        ...


class Grid:
    """
    Implementation of the `grid` class.
    The `grid` is a implicit graph which represents the 2D
    world map layout on which the `pathfinder` object will run.
    During a search, the `pathfinder` object needs to save some critical values. These values are cached within each `node`
    object, and the whole set of nodes are tight inside the `grid` object itself.
    """

    straight_offsets = [
        (1, 0),  # [[W]]
        (-1, 0),  # [[E]]
        (0, 1),  # [[S]]
        (0, -1),  # [[N]]
    ]

    diagonal_offsets = [
        (-1, -1),  # [[NW]],
        (1, -1),  # [[NE]]
        (-1, 1),  # [[SW]],
        (1, 1),  # [[SE]]
    ]

    def __init__(self, map: Map) -> None:
        """
        Inits a new `grid`

        :param table|string map A collision map - (2D array) with consecutive indices (starting at 0 or 1)
        or a `string` with line-break chars (<code>\n</code> or <code>\r</code>) as row delimiters.
        """
        self.map = map
        self.is_annotated: Dict[Walkable, bool] = {}
        (
            self.nodes,
            self.min_x,
            self.max_x,
            self.min_y,
            self.max_y,
        ) = utils.array_to_nodes(map)
        self.width = self.max_x - self.min_x
        self.height = self.max_y - self.min_y

    def annotate(self, walkable: Walkable) -> "Grid":
        """
        Evaluates [clearance](http://aigamedev.com/open/tutorial/clearance-based-pathfinding/#TheTrueClearanceMetric)
        for the whole `grid`. It should be called only once, unless the collision map or the
        __walkable__ attribute changes. The clearance values are calculated and cached within the grid nodes.

        :return pathfinder: (the calling `pathfinder` itself, can be chained)
        """
        for y in range(self.max_y - 1, self.min_y - 1, -1):
            for x in range(self.max_x - 1, self.min_x - 1, -1):
                node = self.get_node_at(x, y)
                assert node
                if self.is_walkable(x, y, walkable):
                    east = self.get_node_at(node.x + 1, node.y)
                    southeast = self.get_node_at(node.x + 1, node.y + 1)
                    south = self.get_node_at(node.x, node.y + 1)

                    if east and southeast and south:
                        m = southeast.clearance[walkable] or 0
                        m = (
                            (south.clearance[walkable] or 0) < m
                            and (south.clearance[walkable] or 0)
                            or m
                        )
                        m = (
                            (east.clearance[walkable] or 0) < m
                            and (east.clearance[walkable] or 0)
                            or m
                        )
                        node.clearance[walkable] = m + 1
                    else:
                        node.clearance[walkable] = 1
                else:
                    node.clearance[walkable] = 0
        self.is_annotated[walkable] = True
        return self

    def is_walkable(
        self,
        x: int,
        y: int,
        walkable: Optional[Walkable] = None,
        clearance: Optional[int] = None,
    ) -> bool:
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
            assert node

            # In this context, a walkable is representing the entity
            # that is trying to get clearance through the node
            node_clearance = node.get_clearance(walkable)
            assert node_clearance
            has_enough_clearance = node_clearance >= clearance

        try:
            return walkable(node_value) and has_enough_clearance
        except TypeError:
            return node_value == walkable and has_enough_clearance

    def get_node_at(self, x: int, y: int) -> Optional[Node]:
        if x < 0 or y < 0:
            return None
        try:
            return self.nodes[y][x]
        except IndexError:
            return None

    def imap(self, f: NodeMapper, *args: Any, **kwargs: Any) -> None:
        """
        Applies a function over all nodes of the grid. The return of the function should be a Node.
        """
        for i, nodes in enumerate(self.nodes):
            for j, node in enumerate(nodes):
                self.nodes[i][j] = f(node, *args, **kwargs)

    def get_neighbours(
        self,
        node: Node,
        walkable: Walkable,
        allow_diagonal: bool = False,
        allow_tunneling: bool = False,
        clearance: bool = False,
    ) -> List[Node]:
        """
        Returns neighbours. The returned value is an array of walkable nodes neighbouring a given `node`.

        :param node: a given `node`
        :param walkable: string|int|func walkable the value for walkable locations in the collision map array (see @{Grid:new}).
        :param allow_diagonal: allowDiagonal when true, allows adjacent nodes are included (8-neighbours).
        :param allow_tunneling: When true, allows the `pathfinder` to tunnel through walls when heading diagonally.
        :param clearance: When given, will prune for the neighbours set all nodes having a clearance value lower than the passed-in value
        :return: an array of nodes neighbouring a given node
        """
        is_walkable = partial(self.is_walkable, walkable=walkable, clearance=clearance)

        neighbours = []
        for offsetX, offsetY in self.straight_offsets:
            n = self.get_node_at(node.x + offsetX, node.y + offsetY)
            if n and is_walkable(n.x, n.y):
                neighbours.append(n)

        if not allow_diagonal:
            return neighbours

        def at_least_one_adjacent_node_in_diagonal_direction_is_walkable(
            offsetX: int, offsetY: int
        ) -> bool:
            n1 = self.get_node_at(node.x + offsetX, node.y)
            n2 = self.get_node_at(node.x, node.y + offsetY)

            if not n1 or not n2:
                return False

            return is_walkable(n1.x, n1.y) or is_walkable(n2.x, n2.y)

        for offsetX, offsetY in self.diagonal_offsets:
            n = self.get_node_at(node.x + offsetX, node.y + offsetY)
            if n and is_walkable(n.x, n.y):
                if (
                    allow_tunneling
                    or at_least_one_adjacent_node_in_diagonal_direction_is_walkable(
                        offsetX, offsetY
                    )
                ):
                    neighbours.append(n)

        return neighbours
