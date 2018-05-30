import re

from node import Node
from path import Path


def trace_back_path(finder, node, start_node):
    path = Path()
    path.grid = finder.grid
    while True:
        if node.parent:
            path.nodes.insert(0, node)
            node = node.parent
        else:
            path.nodes.insert(0, start_node)
            return path


def array_to_nodes(map):
    min_x = 0
    min_y = 0
    max_y = height = len(map)
    max_x = width = len(map[0])

    nodes = [[Node(x, y) for x in range(width)] for y in range(height)]
    return nodes, min_x, max_x, min_y, max_y

def get_array_bounds(map):
    pass


def string_map_to_array(string):
    array_map = []
    for line in string.splitlines():
        stripped_line = line.strip()
        if stripped_line:
            array_map.append(list(stripped_line))

    return array_map
