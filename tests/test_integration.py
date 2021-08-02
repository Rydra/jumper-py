import pytest
from hamcrest import *

import heuristics
from grid import Grid
from heuristics import cardinal_intercardinal
from mytypes.mytypes import Map
from pathfinder import Pathfinder
from properties import AgentCharacteristics
from search import astar, jps, thetastar


@pytest.fixture
def all_heuristics():
    return [
        heuristics.euclidean,
        heuristics.cardinal_intercardinal,
        heuristics.diagonal,
        heuristics.manhattan,
    ]


class TestIntegration:
    def test_clearance_metrics_calculation(self):
        """See Figure 10 at http://aigamedev.com/open/tutorial/clearance-based-pathfinding/"""
        map = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 2, 0],
            [0, 0, 1, 1, 1, 0, 0, 2, 0, 0],
            [0, 0, 0, 1, 1, 0, 2, 0, 0, 2],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        walkable = lambda v: v != 2

        grid = Grid(map).annotate(walkable)
        output = grid.get_clearance_grid(walkable=walkable)

        expected_output = [
            [6, 6, 5, 5, 4, 4, 4, 3, 2, 1],
            [6, 5, 5, 4, 4, 3, 3, 3, 2, 1],
            [6, 5, 4, 4, 3, 3, 2, 2, 2, 1],
            [6, 5, 4, 3, 3, 2, 2, 1, 1, 1],
            [6, 5, 4, 3, 2, 2, 1, 1, 0, 1],
            [5, 5, 4, 3, 2, 1, 1, 0, 1, 1],
            [4, 4, 4, 3, 2, 1, 0, 2, 1, 0],
            [3, 3, 3, 3, 3, 3, 3, 2, 1, 0],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

        assert output == expected_output

    def test_clearance_metrics_calculation2(self):
        """https://harablog.wordpress.com/2009/01/29/clearance-based-pathfinding/"""
        map = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
            [0, 0, 2, 0, 0, 0, 0, 0, 2, 0],
            [0, 0, 2, 2, 2, 0, 0, 2, 0, 0],
            [0, 0, 0, 2, 2, 0, 2, 0, 0, 2],
            [0, 0, 0, 0, 2, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        walkable = lambda v: v != 2

        grid = Grid(map).annotate(walkable)
        output = grid.get_clearance_grid(walkable)

        expected_output = [
            [3, 3, 3, 3, 4, 3, 2, 1, 1, 1],
            [3, 2, 2, 2, 4, 3, 2, 1, 0, 1],
            [2, 2, 1, 1, 3, 3, 2, 2, 2, 1],
            [2, 1, 1, 0, 2, 2, 2, 1, 1, 1],
            [2, 1, 0, 1, 1, 2, 1, 1, 0, 1],
            [2, 1, 0, 0, 0, 1, 1, 0, 1, 1],
            [3, 2, 1, 0, 0, 1, 0, 2, 1, 0],
            [3, 3, 2, 1, 0, 3, 3, 2, 1, 0],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

        assert_that(output, contains_exactly(*expected_output))

    def test_astar_intercardinal_search(self):
        map = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 2, 0],
            [0, 0, 1, 1, 1, 0, 0, 2, 0, 0],
            [0, 0, 0, 1, 1, 0, 2, 0, 0, 2],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        # Make it walkable only on tiles with a 2
        walkable = lambda v: v != 2

        # We need to annotate the clearance on the grid for later use in our pathfindings
        grid = Grid(map).annotate(walkable)
        finder = Pathfinder(astar.search)

        agent_characteristics = AgentCharacteristics(walkable=walkable, clearance=2)

        path = finder.get_path(
            grid,
            (0, 0),
            (8, 8),
            agent_characteristics=agent_characteristics,
            heuristic=cardinal_intercardinal,
        )

        X = "x"
        marked_map = [
            [X, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, X, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, X, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, X, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, X, 0, 0, 0, 2, 0],
            [0, 0, 1, 1, X, 0, 0, 2, 0, 0],
            [0, 0, 0, 1, 1, X, 2, 0, 0, 2],
            [0, 0, 0, 0, 1, 0, X, X, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, X, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        self._assert_the_resulting_path_nodes_should_be_like(marked_map, path)

    @pytest.mark.skip(reason="TODO")
    def test_astar_large_map(self, datadir):
        # Make it walkable only if
        walkable = lambda v: v != 2

        map = (datadir / "large_map_hard.map").read_text()
        map = map.replace("@", "2").replace("T", "1").replace(".", "0")

        grid = Grid(map).annotate(walkable)
        finder = Pathfinder(astar.search)

        agent_characteristics = AgentCharacteristics(walkable=walkable, clearance=2)
        finder.get_path(
            grid,
            (0, 0),
            (8, 8),
            agent_characteristics,
            heuristic=cardinal_intercardinal,
        )

    def test_astar_all_heuristics_should_return_a_similar_path(self, all_heuristics):
        map = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 2, 0],
            [0, 0, 1, 1, 1, 0, 0, 2, 0, 0],
            [0, 0, 0, 1, 1, 0, 2, 0, 0, 2],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        walkable = lambda v: v != 2

        grid = Grid(map).annotate(walkable)
        finder = Pathfinder(astar.search)

        startx, starty = 0, 0
        endx, endy = 8, 8

        paths = []

        agent_characteristics = AgentCharacteristics(walkable=walkable, clearance=2)
        for heuristic in all_heuristics:
            paths.append(
                finder.get_path(
                    grid,
                    (startx, starty),
                    (endx, endy),
                    agent_characteristics,
                    heuristic=heuristic,
                )
            )

        num_nodes = len(paths[0].nodes)
        assert all(len(path.nodes) == num_nodes for path in paths)

    def test_thetastar(self):
        map = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 2, 0],
            [0, 0, 1, 1, 1, 0, 0, 2, 0, 0],
            [0, 0, 0, 1, 1, 0, 2, 0, 0, 2],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        walkable = lambda v: v != 2

        grid = Grid(map).annotate(walkable)
        finder = Pathfinder(thetastar.search)

        startx, starty = 0, 0
        endx, endy = 8, 8
        agent_characteristics = AgentCharacteristics(walkable=walkable, clearance=2)

        path = finder.get_path(
            grid,
            (startx, starty),
            (endx, endy),
            agent_characteristics,
            heuristic=heuristics.diagonal,
        )

        X = "x"
        marked_map = [
            [X, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 2, 0],
            [0, 0, 1, 1, 0, 0, 0, 2, 0, 0],
            [0, 0, 0, 1, 1, 0, 2, 0, 0, 2],
            [0, 0, 0, 0, 1, 0, X, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, X, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        self._assert_the_resulting_path_nodes_should_be_like(marked_map, path)

    def test_do_a_search_jps(self):
        map: Map = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 2, 0],
            [0, 0, 1, 1, 1, 0, 0, 2, 0, 0],
            [0, 0, 0, 1, 1, 0, 2, 0, 0, 2],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        walkable = lambda v: v != 2

        grid = Grid(map).annotate(walkable)
        finder = Pathfinder(jps.search)

        startx, starty = 0, 0
        endx, endy = 8, 8
        agent_characteristics = AgentCharacteristics(walkable=walkable, clearance=2)

        path = finder.get_path(
            grid,
            (startx, starty),
            (endx, endy),
            agent_characteristics,
            heuristic=cardinal_intercardinal,
        )

        X = "x"
        marked_map = [
            [X, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, X, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, X, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, X, 0, 0, 0, 2, 0],
            [0, 0, 1, 1, X, 0, 0, 2, 0, 0],
            [0, 0, 0, 1, 1, X, 2, 0, 0, 2],
            [0, 0, 0, 0, 1, 0, X, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, X, X, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        self._assert_the_resulting_path_nodes_should_be_like(marked_map, path)

    def _assert_the_resulting_path_nodes_should_be_like(self, marked_map, path):
        for node in path.nodes:
            assert marked_map[node.y][node.x] == "x"

    def test_do_a_search_smaller_corridor(self):
        map = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 2, 1, 0, 0, 0, 0, 0, 2, 0],
            [0, 2, 1, 1, 1, 0, 0, 2, 0, 0],
            [0, 2, 0, 1, 1, 0, 2, 0, 0, 2],
            [0, 2, 0, 0, 1, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        walkable = lambda v: v != 2

        grid = Grid(map).annotate(walkable)
        finder = Pathfinder(astar.search)

        startx, starty = 0, 0
        endx, endy = 0, 8
        agent_characteristics = AgentCharacteristics(walkable=walkable, clearance=2)

        path = finder.get_path(
            grid,
            (startx, starty),
            (endx, endy),
            agent_characteristics,
            heuristic=heuristics.diagonal,
        )

        X = "x"
        marked_map = [
            [X, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, X, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 2, X, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, X, 1, 0, 0, 0, 0, 0, 0],
            [0, 2, X, 0, 0, 0, 0, 0, 2, 0],
            [0, 2, X, 1, 1, 0, 0, 2, 0, 0],
            [0, 2, X, 1, 1, 0, 2, 0, 0, 2],
            [0, 2, X, 0, 1, 0, 0, 0, 0, 2],
            [X, X, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        self._assert_the_resulting_path_nodes_should_be_like(marked_map, path)
