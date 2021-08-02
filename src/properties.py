from dataclasses import dataclass

from mytypes.walkable import Walkable


@dataclass
class SearchOptions:
    allow_diagonal: bool
    tunneling: bool


@dataclass
class AgentCharacteristics:
    """
    Class that encapsulates the characteristics of an agent
    (e.g. a plane, a human, a car, etc)

    Args:
        :param string|int|func walkable: the value for walkable locations in the collision map array.
          In a nutshell, this tells where the agent can walk.
        :param int clearance: The amount of clearance this agent needs. Basically, it's the size of the agent
    """

    walkable: Walkable
    clearance: int
