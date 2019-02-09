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
