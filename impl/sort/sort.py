def mergesort(arr):
    if len(arr) <= 1:
        return arr

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
