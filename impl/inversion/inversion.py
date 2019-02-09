def brute_force(arr):
    result = 0
    for i in range(0, len(arr) - 1):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                result += 1

    return result


def recursive_merge(arr):
    # TODO
    return 1
