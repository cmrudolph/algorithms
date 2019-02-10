import importlib
import logging
import timeit


def time(impl, name, runs, *args, func=None):
    log = logging.getLogger("timing.time")

    # Benchmark arg generation is going to depend on the implementation being
    # tested. This entry point must exist in all, but we do not know what
    # inputs the implementations expect. Pass whatever unknown arguments
    # we received along and trust the receiver to do something smart.
    log.debug(f"Creating benchmark args with {args}")
    bench_args = impl.adapt_benchmark_args(args)
    log.debug(f"Benchmark args {bench_args}")

    funcs = [f for f in dir(impl) if not f.startswith("_")]
    funcs.remove("adapt_run_args")
    funcs.remove("adapt_benchmark_args")
    funcs.remove(name)

    if func is not None:
        funcs = [f for f in dir(impl) if f == func]

    log.debug(f"Benchmark funcs {funcs}")

    g = {"bench_args": bench_args, "impl": impl}

    for f in funcs:
        # Warm up pass
        code = f"impl.{f}(**bench_args)"
        timeit.timeit(code, globals=g, number=int(1))

    results = []
    for f in funcs:
        # Dynamically invoke the func under test passing in the benchmark
        # arguments that we computed ahead of time
        code = f"impl.{f}(**bench_args)"
        sec = timeit.timeit(code, globals=g, number=int(runs))
        ops = int(runs / sec)
        full = f"{name}.{f}"

        r = f"{full:<30} {runs:<10} {sec:.10f} sec {ops:>15} ops/sec"
        results.append(r)

    return results
