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
        c_arr = self._wrapper.to_c_int_array(arr)
        self._lib.mergesort(c_arr, len(arr))
        result = self._wrapper.to_py_int_list(c_arr, len(arr))
        return result

    def c_qsort_builtin(self, arr):
        c_arr = self._wrapper.to_c_int_array(arr)
        self._lib.qsort_builtin(c_arr, len(arr))
        result = self._wrapper.to_py_int_list(c_arr, len(arr))
        return result

    def py_mergesort(self, arr):
        return sort.mergesort(arr)

    def py_builtin(self, arr):
        arr.sort()
        return arr

    def create_benchmark_args(self, *args):
        mode = args[0]
        length = int(args[1])

        if mode == "sorted":
            # EXAMPLE: [1, 2, 3, 4, 5]
            return list(range(1, length + 1))
        elif mode == "reversed":
            # EXAMPLE: [5, 4, 3, 2, 1]
            return list(range(length, 0, -1))
        else:
            # EXAMPLE: [4, 2, 1, 5, 3]
            return random.sample(range(1, length + 1), length)
