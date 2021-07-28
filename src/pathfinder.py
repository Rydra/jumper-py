from typing import Any, Optional, Dict

import path
from grid import Grid
from heuristics import manhattan
from interfaces import Searcher
from mytypes.mytypes import Map
from mytypes.walkable import Walkable
from node import Node
from path import Path
from search import astar


class Pathfinder:
    def __init__(
        self, grid: Grid, finder: Searcher, walkable: Walkable, **kwargs: Any
    ) -> None:
        self.grid = grid
        self.finder = finder or astar.search
        self.walkable = walkable  # can be a string, a number or a function
        self.tunneling = kwargs.get("tunneling", False)
        self.heuristic = kwargs.get("heuristic") or manhattan
        self.allow_diagonal = True
        self.to_clear: Dict[Node, bool] = {}

    def annotate_grid(self) -> "Pathfinder":
        self.grid.annotate(self.walkable)
        return self

    def get_path(
        self,
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
        clearance: int = 1,
        **kwargs: Any
    ) -> Optional[Path]:
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

        _end_node = self.finder(
            self,
            start_node,
            end_node,
            clearance,
            self.to_clear,
            heuristic=self.heuristic,
            **kwargs
        )
        if _end_node:
            return path.trace_back_path(self.grid, _end_node, start_node)
        else:
            return None

    def reset(self) -> None:
        for node, _ in self.to_clear.items():
            node.reset()
        self.to_clear = {}

    def get_clearance_grid(self, walkable: Walkable) -> Map:
        output = []
        for y in range(self.grid.height):
            row = []
            for x in range(self.grid.width):
                node = self.grid.get_node_at(x, y)
                row.append(node.get_clearance(walkable))
            output.append(row)

        return output
