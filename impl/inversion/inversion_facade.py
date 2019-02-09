import random
from impl.inversion import inversion


class InversionFacade:
    """
    Facade exposing all the necessary functionality to use this
    implementation for testing/benchmarking purposes.
    """
    def py_brute_force(self, arr):
        return inversion.brute_force(arr)

    def py_recursive_merge(self, arr):
        # We sort the array during the operation and do not want to mutate
        # the original.
        copy = arr[:]
        return inversion.recursive_merge(copy)

    def adapt_run_args(self, raw_args):
        # RUN: Echo back the specified values as integers in a list
        arr = [int(a) for a in raw_args]
        return {"arr": arr}

    def adapt_benchmark_args(self, raw_args):
        # BENCHMARK: Generate and return a list of length N
        mode = raw_args[0]
        length = int(raw_args[1])

        if mode == "sorted":
            arr = list(range(1, length + 1))
        elif mode == "reversed":
            arr = list(range(length, 0, -1))
        elif mode == "zero":
            arr = [0] * length
        else:
            arr = random.sample(range(1, length + 1), length)

        return {"arr": arr}
