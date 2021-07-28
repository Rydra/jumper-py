from typing import Dict, Optional

from heuristics import euclidean
from interfaces import Heuristic
from node import Node
from properties import FinderProperties
from search import astar


def line_of_sight(
    node: Node, neighbour: Node, finder: FinderProperties, clearance: int
) -> bool:
    x0, y0 = node.x, node.y
    x1, y1 = neighbour.x, neighbour.y
    dx, dy = abs(x1 - x0), abs(y1 - y0)
    err = dx - dy
    sx = 1 if (x0 < x1) else -1
    sy = 1 if (y0 < y1) else -1

    while True:
        if not finder.grid.is_walkable(x0, y0, finder.walkable, clearance):
            return False

        if x0 == x1 and y0 == y1:
            break

        e2 = 2 * err
        if e2 > -dy:
            err = err - dy
            x0 = x0 + sx

        if e2 < dx:
            err += dx
            y0 += sy

    return True


def compute_cost(
    node: Node, neighbour: Node, finder: FinderProperties, clearance: int
) -> None:
    parent = node.parent or node
    mp_cost = euclidean(neighbour, parent)
    if line_of_sight(parent, neighbour, finder, clearance):
        if parent.g + mp_cost < neighbour.g:
            neighbour.parent = parent
            neighbour.g = parent.g + mp_cost

    else:
        m_cost = euclidean(neighbour, node)
        if node.g + m_cost < neighbour.g:
            neighbour.parent = node
            neighbour.g = node.g + m_cost


def search(
    finder: FinderProperties,
    start_node: Node,
    end_node: Node,
    clearance: int,
    to_clear: Dict[Node, bool],
    override_heuristic: Optional[Heuristic] = None,
) -> Optional[Node]:
    return astar.search(
        finder,
        start_node,
        end_node,
        clearance,
        to_clear,
        override_heuristic,
        compute_cost,
    )
