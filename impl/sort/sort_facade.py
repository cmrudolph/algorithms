import random
from impl.sort import sort


class SortFacade:
    """
    Facade exposing all the necessary functionality to use this
    implementation for testing/benchmarking purposes.
    """
    def __init__(self, ffi_wrapper):
        self._wrapper = ffi_wrapper
        self._lib = ffi_wrapper.lib

    def c_mergesort(self, arr):
        c_arr = self._wrapper.to_c_array("int[]", arr)
        self._lib.mergesort(c_arr, len(arr))
        result = self._wrapper.to_py_list(c_arr, len(arr))
        return result

    def c_qsort_builtin(self, arr):
        c_arr = self._wrapper.to_c_array("int[]", arr)
        self._lib.qsort_builtin(c_arr, len(arr))
        result = self._wrapper.to_py_list(c_arr, len(arr))

        return result

    def py_mergesort(self, arr):
        result = arr[:]
        sort.mergesort(result)
        return result

    def py_builtin(self, arr):
        result = arr[:]
        result.sort()
        return result

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
