#!/usr/bin/env python3

import ffi
import importlib
import sys
import timeit

if __name__ == "__main__":
    """
    In its current, rough form, default to running a custom benchmark
    function for the specified module. This has a lot of room for improvement,
    but it lets us run code in a timed fashion for now.
    """
    short_name = sys.argv[1]
    iterations = int(sys.argv[2])

    print(f"Benchmarking {short_name} cases with {iterations} iterations")

    wrapper = ffi.FFIWrapper.create(short_name)

    # Convention 1: Assume there is a file called [NAME]/[NAME]_bench.py.
    mod_name = f"{short_name}.{short_name}_bench"
    mod = importlib.import_module(mod_name)

    # Convention 2: Assume there is a setup function to invoke.
    setup_obj = mod.setup(wrapper)

    funcs = [f for f in dir(mod) if f.startswith("benchmark_")]
    funcs.sort()

    for f in funcs:
        f_trimmed = f.replace("benchmark_", "")
        # Convention 3: Assume there is a benchmark function to invoke.
        code = f"mod.{f}(wrapper, setup_obj)"
        setup = "from __main__ import setup_obj, mod, wrapper"
        print(f"{f_trimmed:<25}: ", end="")
        print(timeit.timeit(code, setup=setup, number=int(iterations)))
