from typing import Dict, Optional, Protocol

from grid import Grid
from node import Node
from properties import AgentCharacteristics, SearchOptions


class Heuristic(Protocol):
    def __call__(self, nodeA: Node, nodeB: Node) -> float:
        ...


class CostEvaluator(Protocol):
    def __call__(
        self,
        node: Node,
        neighbour: Node,
        grid: Grid,
        agent_characteristics: Optional[AgentCharacteristics],
    ) -> None:
        ...


class Searcher(Protocol):
    def __call__(
        self,
        grid: Grid,
        finder: SearchOptions,
        start_node: Node,
        end_node: Node,
        agent_characteristics: AgentCharacteristics,
        to_clear: Dict[Node, bool],
        heuristic: Heuristic,
        cost_eval: Optional[CostEvaluator] = None,
    ) -> Optional[Node]:
        ...
