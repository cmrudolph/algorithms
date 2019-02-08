def mergesort(arr):
    if len(arr) <= 1:
        return arr

    middle = len(arr) // 2
    half1 = arr[:middle]
    half2 = arr[middle:]

    mergesort(half1)
    mergesort(half2)

    idx1 = 0
    idx2 = 0

    for i in range(len(arr)):
        if idx1 < len(half1) and (idx2 == len(half2) or half1[idx1] < half2[idx2]):
            arr[i] = half1[idx1]
            idx1 += 1
        else:
            arr[i] = half2[idx2]
            idx2 += 1

    return arr
