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

    # C library sources (foo.c, foo.h)
    ffi = ffi.FFIWrapper.create(short_name)

    # PY wrapper module (foo.py)
    mod = importlib.import_module(short_name + "." + short_name)

    # PY wrapper class (foo.Foo)
    wrapper_type = getattr(mod, short_name.title())
    wrapper_inst = wrapper_type(ffi)

    # Benchmark all non 'dunder' methods in the wrapper class
    funcs = [f for f in dir(wrapper_type) if not f.startswith("__")]
    print(funcs)
    funcs.remove("get_benchmark_args")
    funcs.sort()

    args = wrapper_inst.get_benchmark_args()

    for f in funcs:
        code = f"wrapper_inst.{f}(*args)"
        setup = "from __main__ import args, wrapper_inst"
        print(f"{f:<25}: ", end="")
        print(timeit.timeit(code, setup=setup, number=int(iterations)))
