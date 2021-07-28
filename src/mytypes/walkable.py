from typing import Union, Callable

Walkable = Union[Callable[[int], int], int, str]
