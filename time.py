#!/usr/bin/env python3

import argparse
import importlib
import logging
import timeit
from util.implementation import ImplementationFactory

if __name__ == "__main__":
    """
    Executes a particular function many times, collecting timings and showing
    metrics when finished.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("func")
    parser.add_argument("runs", type=int)
    parser.add_argument("--verbose", action="store_true")
    known, unknown = parser.parse_known_args()

    level = logging.DEBUG if known.verbose else logging.WARNING
    logging.basicConfig(level=level)
    log = logging.getLogger("time")
    log.debug(f"Known args are {known} and unknown args are {unknown}")

    facade = ImplementationFactory.create(known.name, True)

    # Benchmark arg generation is going to depend on the implementation being
    # tested. This entry point must exist in all, but we do not know what
    # inputs the implementations expect. Pass whatever unknown arguments
    # we received along and trust the receiver to do something smart.
    log.debug(f"Creating benchmark args with {unknown}")
    bench_args = facade.create_benchmark_args(*unknown)

    # Dynamically invoke the func under test passing in the benchmark
    # arguments that we computed ahead of time
    code = f"facade.{known.func}(*bench_args)"
    setup = "from __main__ import bench_args, facade"
    sec = timeit.timeit(code, setup=setup, number=int(known.runs))
    ops = int(known.runs / sec)
    full = f"{known.name}.{known.func}"

    print(f"{full:<30} {known.runs:<10} {sec:.10f} sec {ops:>15} ops/sec")
