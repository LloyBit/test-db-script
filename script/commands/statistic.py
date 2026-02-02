"""Benchmark command: runs PrefilteredCommand N times and prints median time."""
import os
import statistics
import sys
import time
from contextlib import contextmanager

from script.commands.base import Command
from script.commands.prefiltered import PrefilteredCommand


@contextmanager
def _suppress_stdout():
    """Context manager that redirects stdout to devnull."""
    orig = sys.stdout
    sys.stdout = open(os.devnull, "w")
    try:
        yield
    finally:
        sys.stdout.close()
        sys.stdout = orig


class StatisticCommand(Command):
    """Runs PrefilteredCommand repeatedly and reports median execution time."""

    def __init__(self, runs: int = 100):
        self.runs = runs

    def run(self):
        times = []
        for _ in range(self.runs):
            with _suppress_stdout():
                start = time.perf_counter()
                PrefilteredCommand().run()
                times.append(time.perf_counter() - start)
        print("Число выполнений:", self.runs)
        print("Медиана:", statistics.median(times))
