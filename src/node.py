from typing import Dict, List, Optional

from mytypes.mytypes import Position
from mytypes.walkable import Walkable


class Node:
    """
    The `node` represents a cell (or a tile) on a collision map. Basically, for each single cell (tile)
    in the collision map passed-in upon initialization, a `node` object will be generated
    and then cached within the `grid`.

    In the following implementation, nodes can be compared using the `<` operator. The comparison is
    made with regards of their `f` cost. From a given node being examined, the `pathfinder` will expand the search
    to the next neighbouring node having the lowest `f` cost. Heaps make use of __lt__ to sort their contents.
    """

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.g: Optional[float] = None
        self.h: Optional[float] = None
        self.opened = False
        self.closed = False
        self.parent: Optional[Node] = None
        self.clearance: Dict[Walkable, Optional[int]] = {}

    @property
    def f(self) -> float:
        return (self.g or 0) + (self.h or 0)

    @property
    def position(self) -> Position:
        return self.x, self.y

    def close(self) -> None:
        self.closed = True

    def open(self) -> None:
        self.opened = True

    def get_clearance(self, walkable: Walkable) -> Optional[int]:
        """
        Returns the amount of true [clearance](http://aigamedev.com/open/tutorial/clearance-based-pathfinding/#TheTrueClearanceMetric)
        for a given `node`
        :param string|int|func walkable: the value for walkable locations in the collision map array.
        :return: int the clearance of the `node`
        """
        return self.clearance.get(walkable)

    def remove_clearance(self, walkable: Walkable) -> None:
        self.clearance[walkable] = None

    def reset(self) -> None:
        self.g = None
        self.h = None
        self.opened = False
        self.closed = False
        self.parent = None

    def __lt__(self, other: "Node") -> bool:
        return self.f < other.f

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"


NodeMap = List[List[Node]]
