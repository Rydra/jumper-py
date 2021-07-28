# Astar algorithm
# This actual implementation of A-star is based on
# [Nash A. & al. pseudocode](http://aigamedev.com/open/tutorials/theta-star-any-angle-paths/)
import heapq
import math
from typing import Any, Optional, Dict, List

from heuristics import euclidean
from interfaces import Heuristic, CostEvaluator
from node import Node
from properties import FinderProperties


def compute_cost(node: Node, neighbour: Node, *args: Any) -> None:
    m_cost = euclidean(
        neighbour, node
    )  # 1 if node.x == neighbour.x or node.y == neighbour.y else 1.41  # Cost of the connection
    if node.g + m_cost < neighbour.g:
        neighbour.parent = node
        neighbour.g = node.g + m_cost


def search(
    finder: FinderProperties,
    start_node: Node,
    end_node: Node,
    clearance: int,
    to_clear: Dict[Node, bool],
    heuristic: Heuristic,
    cost_eval: Optional[CostEvaluator] = None,
) -> Optional[Node]:
    openlist: List[Node] = []  # Actually this should be a priority queue

    def update_vertex(node: Node, neighbour: Node) -> None:
        old_g = neighbour.g
        cmp_cost = cost_eval or compute_cost
        cmp_cost(node, neighbour, finder, clearance)
        if neighbour.g < old_g:
            n_clearance = neighbour.clearance.get(finder.walkable)
            push_this_node = clearance and n_clearance and n_clearance >= clearance
            if push_this_node or not clearance:
                if neighbour.opened:
                    neighbour.opened = False
                neighbour.h = heuristic(end_node, neighbour)
                heapq.heappush(openlist, neighbour)
                neighbour.open()

    start_node.g = 0
    start_node.h = heuristic(end_node, start_node)
    heapq.heappush(openlist, start_node)
    to_clear[start_node] = True
    start_node.opened = True

    while openlist:
        node = heapq.heappop(openlist)
        node.close()
        if node == end_node:
            return node
        neighbours = finder.grid.get_neighbours(
            node, finder.walkable, finder.allow_diagonal, finder.tunneling
        )
        for neighbour in neighbours:
            if not neighbour.closed:
                to_clear[neighbour] = True
                if not neighbour.opened:
                    neighbour.g = math.inf
                    neighbour.parent = None
                update_vertex(node, neighbour)

    return None
