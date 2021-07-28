from typing import NamedTuple

from grid import Grid
from mytypes.walkable import Walkable


class FinderProperties(NamedTuple):
    walkable: Walkable
    grid: Grid
    allow_diagonal: bool
    tunneling: bool
