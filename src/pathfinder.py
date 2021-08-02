from typing import Any, Dict, Optional

import path
from grid import Grid
from heuristics import manhattan
from interfaces import Heuristic, Searcher
from mytypes.mytypes import Position
from node import Node
from path import Path
from properties import AgentCharacteristics, SearchOptions
from search import astar


class Pathfinder:
    def __init__(self, finder: Searcher, **kwargs: Any) -> None:
        self.finder = finder or astar.search
        self.options = SearchOptions(
            allow_diagonal=kwargs.get("allow_diagonal", True),
            tunneling=kwargs.get("tunneling", False),
        )
        self.to_clear: Dict[Node, bool] = {}

    def get_path(
        self,
        grid: Grid,
        start_position: Position,
        end_position: Position,
        agent_characteristics: AgentCharacteristics,
        heuristic: Optional[Heuristic] = None,
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
        start_node = grid.get_node_at(start_position[0], start_position[1])
        end_node = grid.get_node_at(end_position[0], end_position[1])

        _end_node = self.finder(
            grid,
            self.options,
            start_node,
            end_node,
            agent_characteristics,
            self.to_clear,
            heuristic=heuristic or manhattan,
        )
        if _end_node:
            return path.trace_back_path(grid, _end_node, start_node)
        else:
            return None

    def reset(self) -> None:
        for node, _ in self.to_clear.items():
            node.reset()
        self.to_clear = {}
