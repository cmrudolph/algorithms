#include <stdbool.h>
#include <stdio.h>

#define NO_PADDING 0
#define MAX(x, y) (((x) > (y)) ? (x) : (y))

typedef struct {
    int len;
    int *values;
} int_array;

char *cstr_alloc_from_int_array(int_array *arr);
int find_greater_or_equal_power_of_2(int value);
void int_array_add(int_array *accumulator, int_array *a);
int_array *int_array_alloc_zeroed(int len);
int_array *int_array_alloc_from_int(int value);
int_array *int_array_alloc_from_string(char *str, int padded_length);
void int_array_free(int_array *arr);
void int_array_print(int_array *arr);

char *cstr_alloc_from_int_array(int_array *arr)
{
    char *result = malloc(sizeof(char) * arr->len + 1);
    memset(result, '\0', arr->len + 1);

    // Drop all insignificant leading zeroes from the final string.
    int dest = 0;
    bool non_zero_seen = false;
    for (int i = 0; i < arr->len; i++) {
        if (arr->values[i] != 0) {
            non_zero_seen = true;
        }
        if (non_zero_seen || i == (arr->len - 1)) {
            result[dest] = '0' + arr->values[i];
            dest++;
        }
    }

    return result;
}

int find_greater_or_equal_power_of_2(int value)
{
    int i = 1;
    while (i < value) {
        i <<= 1;
    }

    return i;
}

void int_array_add(int_array *accumulator, int_array *a)
{
    int a_idx = a->len - 1;
    for (int i = accumulator->len - 1; i > 0; i--) {
        if (a_idx >= 0) {
            accumulator->values[i] += a->values[a_idx];
            a_idx--;
        }

        // Handle the carry and reduce the current value to [0-9]
        accumulator->values[i-1] += accumulator->values[i] / 10;
        accumulator->values[i] %= 10;
    }
}

int_array *int_array_alloc_zeroed(int len)
{
    int_array *result = malloc(sizeof(int_array));
    result->len = len;
    result->values = malloc(sizeof(int) * len);
    memset(result->values, 0, len * sizeof(int));

    return result;
}

int_array *int_array_alloc_from_int(int value)
{
    int num_digits = 0;
    int temp = value;
    while (temp > 0) {
        num_digits++;
        temp /= 10;
    }

    // Special case where value is zero
    if (num_digits == 0) {
        num_digits += 1;
    }

    int_array *result = int_array_alloc_zeroed(num_digits);

    temp = value;
    for (int i = num_digits - 1; i >= 0; i--) {
        result->values[i] = temp % 10;
        temp /= 10;
    }

    return result;
}

int_array *int_array_alloc_from_string(char *str, int padded_length)
{
    // The result string sometimes needs to be front zero padded to satisfy
    // algorithm assumptions. The length must be big enough for whichever scenario
    // we are dealing with (padded or non).
    int str_len = strlen(str);
    int result_len = MAX(str_len, padded_length);
    int_array *result = int_array_alloc_zeroed(result_len);

    // Copy all the original chars over. Anything not touched will retain its
    // original zero value (zero padded at the front).
    int str_idx = str_len - 1;
    for (int i = result_len - 1; i >= 0; i--) {
        if (str_idx >= 0) {
            result->values[i] = str[str_idx] - '0';
            str_idx--;
        }
    }

    return result;
}

void int_array_free(int_array *arr)
{
    free(arr->values);
    arr->len = 0;
    arr->values = NULL;

    free(arr);
}

void int_array_print(int_array *arr)
{
    for (int i = 0; i < arr->len; i++) {
        printf("%d", arr->values[i]);
    }
    printf("\n");
}

char *multiply_long(char *str1, char *str2)
{
    int_array *a1 = int_array_alloc_from_string(str1, NO_PADDING);
    int_array *a2 = int_array_alloc_from_string(str2, NO_PADDING);

    int result_len = a1->len + a2->len;
    int_array *result = int_array_alloc_zeroed(result_len);

    // Compute from R -> L, just like how the grade school method is done by hand
    for (int i = a1->len - 1; i >= 0; i--) {
        for (int j = a2->len - 1; j >= 0; j--) {
            int result_idx = i + j + 1;

            // Multiply the two digits and break out the components.
            int product = a1->values[i] * a2->values[j];
            int digit = product % 10;
            int initial_carry = product / 10;

            // Update the result array in-place. The update might force a
            // cell to roll over (10+), triggering the need to factor this
            // calculation into the carry.
            result->values[result_idx] += digit;
            int extra_carry = result->values[result_idx] / 10;

            // Perform final updates (reducing the target cell to be < 10
            // and adding in the carry).
            result->values[result_idx] %= 10;
            result->values[result_idx - 1] += (initial_carry + extra_carry);
        }
    }

    int_array_free(a1);
    int_array_free(a2);

    char *result_cstr = cstr_alloc_from_int_array(result);
    free(result);

    return result_cstr;
}

int_array *multiply_recursive_internal(int_array *a1, int_array *a2, int off1, int off2, int len)
{
    if (len == 1) {
        int x = a1->values[off1];
        int y = a2->values[off2];
        int base_product = x * y;

        int_array *base_result = int_array_alloc_from_int(base_product);
        return base_result;
    }

    int half = len / 2;

    int_array *ac = multiply_recursive_internal(a1, a2, off1, off2, half);

    // 10^n * ac
    int_array *ac_final = int_array_alloc_zeroed(ac->len + len);
    for (int i = 0; i < ac->len; i++) {
        ac_final->values[i] = ac->values[i];
    }

    int_array *ad = multiply_recursive_internal(a1, a2, off1, off2 + half, half);

    // 10^(n/2) * ad
    int_array *ad_final = int_array_alloc_zeroed(ad->len + half);
    for (int i = 0; i < ad->len; i++) {
        ad_final->values[i] = ad->values[i];
    }

    int_array *bc = multiply_recursive_internal(a1, a2, off1 + half, off2, half);

    // 10^(n/2) * bc
    int_array *bc_final = int_array_alloc_zeroed(bc->len + half);
    for (int i = 0; i < bc->len; i++) {
        bc_final->values[i] = bc->values[i];
    }

    int_array *bd_final = multiply_recursive_internal(a1, a2, off1 + half, off2 + half, half);

    int_array *result = int_array_alloc_zeroed(len * 2 + 1);
    int_array_add(result, ac_final);
    int_array_add(result, ad_final);
    int_array_add(result, bc_final);
    int_array_add(result, bd_final);

    int_array_free(ac);
    int_array_free(ac_final);
    int_array_free(ad);
    int_array_free(ad_final);
    int_array_free(bc);
    int_array_free(bc_final);
    int_array_free(bd_final);

    return result;
}

char *multiply_recursive(char *str1, char *str2)
{
    int len1 = strlen(str1);
    int len2 = strlen(str2);

    int a1_pow_2 = find_greater_or_equal_power_of_2(len1);
    int a2_pow_2 = find_greater_or_equal_power_of_2(len2);
    int max_pow_2 = MAX(a1_pow_2, a2_pow_2);

    int_array *a1 = int_array_alloc_from_string(str1, max_pow_2);
    int_array *a2 = int_array_alloc_from_string(str2, max_pow_2);

    int_array * result = multiply_recursive_internal(a1, a2, 0, 0, max_pow_2);

    char *result_cstr = cstr_alloc_from_int_array(result);
    int_array_free(result);

    return result_cstr;
}