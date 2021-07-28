from typing import Protocol

from grid import Grid
from mytypes.walkable import Walkable


class FinderProperties(Protocol):
    walkable: Walkable
    grid: Grid
    allow_diagonal: bool
    tunneling: bool
