#!/usr/bin/env python3

import argparse
import ffi
import importlib
import logging
import sys
import timeit
import wrapper

if __name__ == "__main__":
    """
    In its current, rough form, default to running a custom benchmark
    function for the specified module. This has a lot of room for improvement,
    but it lets us run code in a timed fashion for now.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("iterations", type=int)
    parser.add_argument("--contains")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    level = logging.DEBUG if args.verbose else logging.WARNING
    logging.basicConfig(level=level)
    log = logging.getLogger("time")
    log.debug(f"Args:{args}")

    print(f"Benchmarking {args.name} cases with {args.iterations} iterations")

    wrapper = wrapper.WrapperFactory.create(args.name, True)

    # Benchmark all non 'dunder' methods in the wrapper class
    funcs = [f for f in dir(wrapper) if not f.startswith("_")]
    funcs.remove("get_benchmark_args")
    funcs.sort()
    if args.contains is not None:
        funcs = [f for f in funcs if args.contains in f]
    log.debug(f"Funcs:{funcs}")

    bench_args = wrapper.get_benchmark_args()

    for f in funcs:
        code = f"wrapper.{f}(*bench_args)"
        setup = "from __main__ import bench_args, wrapper"
        print(f"{f:<25} ", end="")
        result = timeit.timeit(code, setup=setup, number=int(args.iterations))
        ops_per_sec = int(args.iterations / result)
        print(f"{result:.10f} sec {ops_per_sec:>15} ops/sec")
