from mytypes.mytypes import Tuple, List

from node import Node, NodeMap
from mytypes.mytypes import Map


def array_to_nodes(map: Map) -> Tuple[NodeMap, int, int, int, int]:
    min_x = 0
    min_y = 0
    max_y = height = len(map)
    max_x = width = len(map[0])

    nodes = [[Node(x, y) for x in range(width)] for y in range(height)]
    return nodes, min_x, max_x, min_y, max_y


def string_map_to_array(string: str) -> List[List[str]]:
    array_map: List[List[str]] = []
    for line in string.splitlines():
        stripped_line = line.strip()
        if stripped_line:
            array_map.append(list(stripped_line))

    return array_map
