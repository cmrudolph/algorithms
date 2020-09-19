import os
import random
import util

h_file = os.path.join(os.path.dirname(__file__), "sort.h")
c_file = os.path.join(os.path.dirname(__file__), "sort.c")
(ffi, lib) = util.compile("sort", h_file, c_file)

def c_bubblesort(arr):
    c_arr = ffi.new("int[]", arr)
    lib.bubblesort(c_arr, len(arr))
    result = ffi.unpack(c_arr, len(arr))
    return result


def c_insertionsort(arr):
    c_arr = ffi.new("int[]", arr)
    lib.insertionsort(c_arr, len(arr))
    result = ffi.unpack(c_arr, len(arr))
    return result


def c_mergesort(arr):
    c_arr = ffi.new("int[]", arr)
    lib.mergesort(c_arr, len(arr))
    result = ffi.unpack(c_arr, len(arr))
    return result


def c_qsort_builtin(arr):
    c_arr = ffi.new("int[]", arr)
    lib.qsort_builtin(c_arr, len(arr))
    result = ffi.unpack(c_arr, len(arr))
    return result


def c_quicksort(arr):
    c_arr = ffi.new("int[]", arr)
    lib.quicksort(c_arr, len(arr))
    result = ffi.unpack(c_arr, len(arr))
    return result


def py_builtin(arr):
    result = arr[:]
    result.sort()
    return result


def py_mergesort(arr):
    result = arr[:]
    mergesort(result)
    return result


def py_quicksort(arr):
    result = arr[:]
    quicksort(result)
    return result


def adapt_run_args(raw_args):
    # RUN: Echo back the specified values as integers in a list
    arr = [int(a) for a in raw_args]
    return {"arr": arr}


def adapt_benchmark_args(raw_args):
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


def mergesort(arr):
    if len(arr) <= 1:
        return

    middle = len(arr) // 2
    h1 = arr[:middle]
    h2 = arr[middle:]

    mergesort(h1)
    mergesort(h2)

    idx1 = 0
    idx2 = 0

    for i in range(len(arr)):
        if idx1 < len(h1) and (idx2 == len(h2) or h1[idx1] < h2[idx2]):
            arr[i] = h1[idx1]
            idx1 += 1
        else:
            arr[i] = h2[idx2]
            idx2 += 1


def partition(arr, length, offset):
    pivot = arr[offset]
    i = offset + 1
    for j in range(offset + 1, offset + length):
        if arr[j] < pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[offset], arr[i-1] = arr[i-1], arr[offset]
    return i-1


def quicksort_internal(arr, length, offset):
    if length <= 1:
        return

    # Select the pivot at random to produce a more consistent result
    pivot_idx = random.randint(offset, offset + length - 1)
    arr[offset], arr[pivot_idx] = arr[pivot_idx], arr[offset]

    divider = partition(arr, length, offset)

    # Segment left of the pivot
    l_len = divider - offset
    l_offset = offset

    # Segment right of the pivot
    r_len = length - divider + offset - 1
    r_offset = divider + 1

    quicksort_internal(arr, l_len, l_offset)
    quicksort_internal(arr, r_len, r_offset)


def quicksort(arr):
    quicksort_internal(arr, len(arr), 0)
