# type: ignore

# Asyncio version
import asyncio as aio
import threading
from concurrent.futures.thread import ThreadPoolExecutor
from functools import partial, wraps

from grid import Grid
from heuristics import cardinal_intercardinal
from pathfinder import Pathfinder
from profiling.decorators import timewith
from search import astar


def get_path(path_to_do):
    finder = path_to_do[1]
    agent_size = path_to_do[2]
    path_to_do = path_to_do[0]
    return finder.get_path(
        path_to_do[0][0],
        path_to_do[0][1],
        path_to_do[1][0],
        path_to_do[1][1],
        agent_size,
    )


def run_async():
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

    paths = [
        ((0, 0), (8, 8)),
        ((0, 0), (3, 5)),
        ((1, 0), (1, 8)),
        ((0, 0), (8, 8)),
        ((0, 0), (8, 8)),
        ((0, 0), (8, 8)),
        ((0, 0), (8, 8)),
        ((0, 0), (8, 8)),
        ((0, 0), (8, 8)),
        ((0, 0), (8, 8)),
        ((0, 0), (8, 8)),
        ((0, 0), (8, 8)),
        ((0, 0), (8, 8)),
        ((0, 0), (8, 8)),
    ] * 100
    agent_size = 2

    with timewith():
        grid = Grid(map)
        finder = Pathfinder(astar.search, heuristic=cardinal_intercardinal)
        grid.annotate(walkable)

        # Compute all the paths serially
        computed_paths = []
        for start, end in paths:
            computed_paths.append(
                finder.get_path(start[0], start[1], end[0], end[1], agent_size)
            )

    assert len(computed_paths) == len(paths)

    # Multithreaded version. It should take almost the same as the previous one (or more due to overhead of threads)
    # since computing the path is a purely CPU bound operation.
    # Node: The options IS NOT threadsafe
    class PathFinderLocal(threading.local):
        def __init__(self):
            print("Initializing local")
            local_grid = Grid(map)
            local_grid.annotate(walkable)
            self.finder = Pathfinder(astar.search, heuristic=cardinal_intercardinal)

    local_finder = PathFinderLocal()

    with timewith():
        with ThreadPoolExecutor(max_workers=5) as executor:

            def _(path_to_do):
                return local_finder.finder.get_path(
                    path_to_do[0][0],
                    path_to_do[0][1],
                    path_to_do[1][0],
                    path_to_do[1][1],
                    agent_size,
                )

            computed_paths = executor.map(_, paths)

    assert len(list(computed_paths)) == len(paths)

    # Multiprocessing version. This one should actually be more performant
    # with timewith():
    #     grid = Grid(map)
    #     options = Pathfinder(grid, astar.search, walkable, heuristic=cardinal_intercardinal)
    #     options.annotate_grid()
    #
    #     with ProcessPoolExecutor(max_workers=2) as executor:
    #         computed_paths = executor.map(get_path, [(p, options, agent_size) for p in paths[:2]])

    # assert len(list(computed_paths)) == len(paths)


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

paths = [
    ((0, 0), (8, 8)),
    ((0, 0), (3, 5)),
    ((1, 0), (1, 8)),
    ((0, 0), (8, 8)),
    ((0, 0), (8, 8)),
    ((0, 0), (8, 8)),
    ((0, 0), (8, 8)),
    ((0, 0), (8, 8)),
    ((0, 0), (8, 8)),
    ((0, 0), (8, 8)),
    ((0, 0), (8, 8)),
    ((0, 0), (8, 8)),
    ((0, 0), (8, 8)),
    ((0, 0), (8, 8)),
] * 100

agent_size = 2


def async_wrap(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = aio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)

    return run


async def run_async_2():
    with timewith("async"):
        grid = Grid(map)
        finder = Pathfinder(astar.search, heuristic=cardinal_intercardinal)
        grid.annotate(walkable)
        get_path_async = async_wrap(finder.get_path)

        # Compute all the paths serially
        computed_paths = []
        tasks = []
        for start, end in paths:
            tasks.append(get_path_async(start[0], start[1], end[0], end[1], agent_size))

        await aio.gather(*tasks)

    assert len(computed_paths) == len(paths)


run_async()
aio.run(run_async_2())
