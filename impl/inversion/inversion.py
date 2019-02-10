import random


def py_brute_force(arr):
    return brute_force(arr)


def py_recursive_merge(arr):
    # We sort the array during the operation and do not want to mutate
    # the original.
    copy = arr[:]
    return recursive_merge(copy)


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


def brute_force(arr):
    result = 0
    for i in range(0, len(arr) - 1):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                result += 1

    return result


def recursive_merge(arr):
    if len(arr) <= 1:
        return 0

    middle = len(arr) // 2
    h1 = arr[:middle]
    h2 = arr[middle:]

    left_inv = recursive_merge(h1)
    right_inv = recursive_merge(h2)

    idx1 = 0
    idx2 = 0
    split_inv = 0

    for i in range(len(arr)):
        if idx1 < len(h1) and (idx2 == len(h2) or h1[idx1] <= h2[idx2]):
            arr[i] = h1[idx1]
            idx1 += 1
        else:
            arr[i] = h2[idx2]
            idx2 += 1
            split_inv += len(h1) - idx1

    return left_inv + right_inv + split_inv
