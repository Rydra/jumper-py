import heuristics
from grid import Grid
from heuristics import cardinal_intercardinal
from pathfinder import Pathfinder
from search import astar, jps


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
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
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
            [6, 6, 5, 5, 4, 4, 4, 3, 2, 1],
            [6, 5, 5, 4, 4, 3, 3, 3, 2, 1],
            [6, 5, 4, 4, 3, 3, 2, 2, 2, 1],
            [6, 5, 4, 3, 3, 2, 2, 1, 2, 1],
            [6, 5, 4, 3, 2, 2, 1, 2, 0, 1],
            [5, 5, 4, 3, 2, 1, 3, 0, 1, 1],
            [4, 4, 4, 4, 4, 4, 0, 2, 1, 0],
            [3, 3, 3, 3, 3, 3, 3, 3, 2, 0],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

        assert output == expected_output

    def test_do_a_search(self):
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
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        walkable = lambda v: v != 2

        grid = Grid(map)
        finder = Pathfinder(grid, astar.search, walkable, heuristic=cardinal_intercardinal)
        finder.annotate_grid()

        startx, starty = 0, 0
        endx, endy = 8, 8
        agent_size = 2

        path = finder.get_path(startx, starty, endx, endy, agent_size)

        if path:
            for i, node in enumerate(path):
                print(f'Step {i}. ({node.position})')

    def test_do_a_search_jps(self):
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
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        walkable = lambda v: v != 2

        grid = Grid(map)
        finder = Pathfinder(grid, jps.search, walkable, heuristic=cardinal_intercardinal)
        finder.annotate_grid()

        startx, starty = 0, 0
        endx, endy = 8, 8
        agent_size = 2

        path = finder.get_path(startx, starty, endx, endy, agent_size)

        if path:
            for i, node in enumerate(path):
                print(f'Step {i}. ({node.position})')


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
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        walkable = lambda v: v != 2

        grid = Grid(map)
        finder = Pathfinder(grid, astar.search, walkable, heuristic=heuristics.diagonal)
        finder.annotate_grid()

        startx, starty = 0, 0
        endx, endy = 0, 8
        agent_size = 2

        path = finder.get_path(startx, starty, endx, endy, agent_size)

        if path:
            for i, node in enumerate(path):
                print(f'Step {i}. ({node.position})')

    def test_do_a_search_smaller_example(self):
        map = [
            [0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0]
        ]

        walkable = 0

        grid = Grid(map)
        finder = Pathfinder(grid, jps.search, walkable, heuristic=heuristics.diagonal)
        finder.annotate_grid()

        startx, starty = 0, 0
        endx, endy = 4, 0

        path = finder.get_path(startx, starty, endx, endy)

        if path:
            for i, node in enumerate(path):
                print(f'Step {i}. ({node.position})')