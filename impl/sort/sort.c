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
            dest[i] = src1[idx1];
            idx1++;
        }
        else if (idx1 == len1) {
            dest[i] = src2[idx2];
            idx2++;
        }
        else if (src1[idx1] < src2[idx2]) {
            dest[i] = src1[idx1];
            idx1++;
        }
        else {
            dest[i] = src2[idx2];
            idx2++;
        }
        i++;
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