# type: ignore

import cProfile
import os
from contextlib import contextmanager

import yappi
from pyinstrument import Profiler

from pathlib import Path
from time import perf_counter, process_time


@contextmanager
def instrument(filename="results"):
    profiler = Profiler()
    directory = Path("profiling/results/")
    try:
        profiler.start()
        yield
    finally:
        profiler.stop()
        directory.mkdir(parents=True, exist_ok=True)
        path = os.path.join(directory, f"{filename}.html")
        with open(path, "w") as fs:
            fs.write(profiler.output_html(timeline=True))


@contextmanager
def profile(filename="results", engine="yappi", clock="wall", output_type="pstat"):
    directory = Path("profiling/results/")
    directory.mkdir(parents=True, exist_ok=True)
    path = os.path.join(directory, f"{filename}.prof")

    if engine == "yappi":
        yappi.set_clock_type(clock)
        try:
            yappi.start(builtins=True, profile_threads=False)
            yield
        finally:
            yappi.stop()
            stats = yappi.get_func_stats()
            stats.print_all()
            stats.save(path, type=output_type)
    else:
        profile = cProfile.Profile()
        try:
            profile.enable()
            yield
        finally:
            profile.disable()
            profile.print_stats()
            profile.dump_stats(path)


class timewith:
    def __init__(self, name="", cpu_time=False):
        self.name = name
        self.cpu_time = cpu_time
        self.time_func = perf_counter if not cpu_time else process_time
        self.start = self.time_func()
        self.end = None

    @property
    def elapsed(self):
        return self.time_func() - self.start

    def checkpoint(self, name=""):
        time = 1000.0 * (self.time_func() - self.start)
        print(f"{self.name} {name} took {time} ms".strip())

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.end = self.time_func()
        self.checkpoint("finished")
