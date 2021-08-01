from typing import Callable, Union

Walkable = Union[Callable[[int], int], int, str]
