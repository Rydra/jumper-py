from heuristics import euclidean
from search import astar


def line_of_sight(node, neighbour, finder, clearance):
    x0, y0 = node.x, node.y
    x1, y1 = neighbour.x, neighbour.y
    dx = abs(x1-x0)
    dy = abs(y1-y0)
    err = dx - dy
    sx = (x0 < x1) and 1 or -1
    sy = (y0 < y1) and 1 or -1

    while True:
        if not finder.grid.is_walkable(x0, y0, finder.walkable, finder.tunnel, clearance):
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


def compute_cost(node, neighbour, finder, clearance):
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


def search(finder, start_node, end_node, clearance, to_clear, override_heuristic):
    return astar.search(finder, start_node, end_node, clearance, to_clear, override_heuristic, compute_cost)
