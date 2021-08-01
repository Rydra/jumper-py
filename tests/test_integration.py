import pytest

import heuristics
from grid import Grid
from heuristics import cardinal_intercardinal
from mytypes.mytypes import Map
from pathfinder import Pathfinder
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

        grid = Grid(map)
        grid.annotate(walkable)
        finder = Pathfinder(grid, astar.search, walkable)
        finder.annotate_grid()

        output = []
        for y in range(len(map)):
            row = []
            for x in range(len(map[0])):
                node = grid.get_node_at(x, y)
                row.append(node.get_clearance(walkable))
            output.append(row)

        expected_output = [
            [6, 6, 5, 5, 4, 4, 4, 3, 2, 1],
            [6, 5, 5, 4, 4, 3, 3, 3, 2, 1],
            [6, 5, 4, 4, 3, 3, 2, 2, 2, 1],
            [6, 5, 4, 3, 3, 2, 2, 1, 2, 1],
            [6, 5, 4, 3, 2, 2, 1, 2, 0, 1],
            [5, 5, 4, 3, 2, 1, 3, 0, 1, 1],
            [4, 4, 4, 4, 4, 4, 0, 2, 1, 0],
            [3, 3, 3, 3, 3, 3, 3, 3, 2, 0],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

        assert output == expected_output

    def test_clearance_metrics_calculation2(self):
        """See Figure 10 at http://aigamedev.com/open/tutorial/clearance-based-pathfinding/"""
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

        grid = Grid(map)
        finder = Pathfinder(grid, astar.search, walkable)
        finder.annotate_grid()

        output = []
        for y in range(len(map)):
            row = []
            for x in range(len(map[0])):
                node = grid.get_node_at(x, y)
                row.append(node.get_clearance(walkable))
            output.append(row)

        expected_output = [
            [3, 3, 3, 3, 4, 3, 2, 1, 1, 1],
            [3, 2, 2, 2, 3, 3, 2, 1, 0, 1],
            [2, 2, 1, 1, 3, 3, 2, 2, 2, 1],
            [2, 1, 1, 0, 2, 2, 2, 1, 1, 1],
            [2, 1, 0, 1, 1, 2, 1, 1, 0, 1],
            [2, 1, 0, 0, 0, 1, 1, 0, 1, 1],
            [3, 2, 1, 0, 0, 1, 0, 2, 1, 0],
            [3, 3, 2, 1, 0, 3, 3, 3, 1, 0],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

        assert output == expected_output

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

        # Make it walkable only if
        walkable = lambda v: v != 2

        grid = Grid(map).annotate(walkable)
        finder = Pathfinder(
            grid,
            astar.search,
            walkable,
        )

        path = finder.get_path(
            (0, 0), (8, 8), clearance=2, heuristic=cardinal_intercardinal
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

    def test_astar_large_map(self, datadir):
        # Make it walkable only if
        walkable = lambda v: v != 2

        map = (datadir / "large_map_hard.map").read_text()
        map = map.replace("@", "2").replace("T", "1").replace(".", "0")

        grid = Grid(map).annotate(walkable)
        finder = Pathfinder(
            grid,
            astar.search,
            walkable,
        )

        path = finder.get_path(
            (0, 0), (8, 8), clearance=2, heuristic=cardinal_intercardinal
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

        grid = Grid(map)
        finder = Pathfinder(
            grid, astar.search, walkable, heuristic=cardinal_intercardinal
        )
        finder.annotate_grid()

        startx, starty = 0, 0
        endx, endy = 8, 8
        agent_size = 2

        paths = []

        for heuristic in all_heuristics:
            paths.append(
                finder.get_path(
                    startx, starty, endx, endy, agent_size, heuristic=heuristic
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

        grid = Grid(map)
        finder = Pathfinder(
            grid, thetastar.search, walkable, heuristic=heuristics.diagonal
        )
        finder.annotate_grid()

        startx, starty = 0, 0
        endx, endy = 8, 8
        agent_size = 2

        path = finder.get_path(startx, starty, endx, endy, agent_size)

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

        grid = Grid(map)
        finder = Pathfinder(
            grid, jps.search, walkable, heuristic=cardinal_intercardinal
        )
        finder.annotate_grid()

        startx, starty = 0, 0
        endx, endy = 8, 8
        agent_size = 2

        path = finder.get_path(startx, starty, endx, endy, agent_size)

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

        grid = Grid(map)
        finder = Pathfinder(grid, astar.search, walkable, heuristic=heuristics.diagonal)
        finder.annotate_grid()

        startx, starty = 0, 0
        endx, endy = 0, 8
        agent_size = 2

        path = finder.get_path(startx, starty, endx, endy, agent_size)

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

    def test_do_a_search_smaller_example(self):
        map = [[0, 1, 0, 1, 0], [0, 1, 0, 1, 0], [0, 1, 1, 1, 0], [0, 0, 0, 0, 0]]

        walkable = 0

        grid = Grid(map)
        finder = Pathfinder(grid, jps.search, walkable, heuristic=heuristics.diagonal)
        finder.annotate_grid()

        startx, starty = 0, 0
        endx, endy = 4, 0

        path = finder.get_path(startx, starty, endx, endy)

        if path:
            for i, node in enumerate(path):
                print(f"Step {i}. ({node.position})")
