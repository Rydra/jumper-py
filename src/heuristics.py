"""
Heuristic functions for search algorithms.

A <a href="http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html">distance heuristic</a>
provides an *estimate of the optimal distance cost* from a given location to a target.
As such, it guides the pathfinder to the goal, helping it to decide which route is the best.

This script holds the definition of some built-in heuristics available through jumper.

Distance functions are internally used by the `pathfinder` to evaluate the optimal path
from the start location to the goal.

Jumper features some built-in distance heuristics, namely `MANHATTAN`, `EUCLIDIAN`, `DIAGONAL`, `CARDINTCARD`.
You can also supply your own heuristic function as long as it accepts two Nodes as arguments and return an integer
indicating the distance between both nodes.
"""
import math

sqrt2 = math.sqrt(2)


def manhattan(nodeA, nodeB):
    """
    Manhattan distance.
    <br/>This heuristic is the default one being used by the `pathfinder` object.
    <br/>Evaluates as <code>distance = |dx|+|dy|</code>
    """
    dx = abs(nodeA.x - nodeB.x)
    dy = abs(nodeA.y - nodeB.y)
    return dx + dy


def euclidean(nodeA, nodeB):
    """
    Euclidean distance.
    <br/>Evaluates as <code>distance = squareRoot(dx*dx+dy*dy)</code>
    """
    dx = nodeA.x - nodeB.x
    dy = nodeA.y - nodeB.y
    return math.sqrt(dx * dx + dy * dy)


def diagonal(nodeA, nodeB):
    """
    Diagonal distance.
    <br/>Evaluates as <code>distance = max(|dx|, abs|dy|)</code>
    """
    dx = abs(nodeA.x - nodeB.x)
    dy = abs(nodeA.y - nodeB.y)
    return max(dx, dy)


def cardinal_intercardinal(nodeA, nodeB):
    """
    Cardinal/Intercardinal distance.
    <br/>Evaluates as <code>distance = min(dx, dy)*squareRoot(2) + max(dx, dy) - min(dx, dy)</code>
    """
    dx = abs(nodeA.x - nodeB.x)
    dy = abs(nodeA.y - nodeB.y)

    return min(dx, dy) * sqrt2 + max(dx, dy) - min(dx, dy)
