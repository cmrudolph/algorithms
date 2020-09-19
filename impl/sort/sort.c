#include <stdbool.h>
#include <stdlib.h>

void mergesort_internal(int *src, int *dest, int len)
{
    if (len <= 1) {
        return;
    }

    int mid = len / 2;
    int *src1 = src;
    int *src2 = src + mid;
    int *dest1 = dest;
    int *dest2 = dest + mid;
    int len1 = mid;
    int len2 = len - mid;

    mergesort_internal(dest1, src1, len1);
    mergesort_internal(dest2, src2, len2);

    int i = 0;
    int idx1 = 0;
    int idx2 = 0;
    while (idx1 < len1 || idx2 < len2) {
        if (idx2 == len2) {
            while (idx1 < len1) {
                dest[i++] = src1[idx1++];
            }
        }
        else if (idx1 == len1) {
            while (idx2 < len2) {
                dest[i++] = src2[idx2++];
            }
        }
        else if (src1[idx1] < src2[idx2]) {
            dest[i++] = src1[idx1++];
        }
        else {
            dest[i++] = src2[idx2++];
        }
    }
}

void bubblesort(int *arr, int len)
{
    for (int i = 0; i < len; i++)
    {
        bool swapped = false;

        for (int j = 0; j < len - 1; j++)
        {
            if (arr[j] > arr[j+1])
            {
                int temp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = temp;
                swapped = true;
            }
        }

        if (!swapped)
        {
            // Short-circuit the operation if no swaps were performed. This means we ended up
            // with a sorted list (potentially) early.
            break;
        }
    }
}

void insertionsort(int *arr, int len)
{
    for (int i = 1; i < len; i++)
    {
        int curr = arr[i];
        int j = i - 1;

        while (j >= 0 && arr[j] > curr)
        {
            arr[j + 1] = arr[j];
            j = j - 1;
        }
        arr[j + 1] = curr;
    }
}

void mergesort(int *arr, int len)
{
    int *result = malloc(len * sizeof(int));
    memcpy(result, arr, len * sizeof(int));
    mergesort_internal(arr, result, len);
    memcpy(arr, result, len * sizeof(int));
    free(result);
}

int cmpfunc (const void *a, const void *b)
{
   return *(int *)a - *(int *)b;
}

void qsort_builtin(int *arr, int len)
{
    qsort(arr, len, sizeof(int), cmpfunc);
}

void swap(int *x, int *y)
{
    int tmp = *x;
    *x = *y;
    *y = tmp;
}

int partition(int *arr, int len)
{
    int pivot = arr[0];
    int i = 1;
    for (int j = 1; j < len; j++) {
        if (arr[j] < pivot) {
            swap(&arr[j], &arr[i]);
            i++;
        }
    }

    swap(&arr[0], &arr[i-1]);
    return i-1;
}

void quicksort(int *arr, int len)
{
    if (len <= 1) {
        return;
    }

    // Select the pivot at random to produce a more consistent result
    int pivot_idx = rand() % len;
    swap(&arr[0], &arr[pivot_idx]);

    int divider = partition(arr, len);
    quicksort(arr, divider);
    quicksort(arr + divider + 1, len - divider - 1);
}