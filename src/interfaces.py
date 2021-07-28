from typing import Protocol, Optional, Dict, Any

from node import Node
from properties import FinderProperties


class Heuristic(Protocol):
    def __call__(self, nodeA: Node, nodeB: Node) -> float:
        ...


class CostEvaluator(Protocol):
    def __call__(self, node: Node, neighbour: Node, *args: Any, **kwargs: Any) -> None:
        ...


class Searcher(Protocol):
    def __call__(
        self,
        finder: FinderProperties,
        start_node: Node,
        end_node: Node,
        clearance: int,
        to_clear: Dict[Node, bool],
        heuristic: Optional[Heuristic] = None,
        cost_eval: Optional[CostEvaluator] = None,
    ) -> Optional[Node]:
        ...
