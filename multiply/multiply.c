#include <stdbool.h>

int *numeric_string_to_int_array(char *str, int len)
{
    int *result = malloc(sizeof(int) * len);

    for (int i = 0; i < len; i++) {
        result[i] = str[i] - '0';
    }

    return result;
}

char *int_array_to_numeric_string(int *vals, int len)
{
    char *result = malloc(sizeof(char) * len + 1);
    memset(result, '\0', len + 1);

    // Drop all insignificant leading zeroes from the final string.
    int dest = 0;
    bool non_zero_seen = false;
    for (int i = 0; i < len; i++) {
        if (vals[i] != 0) {
            non_zero_seen = true;
        }
        if (non_zero_seen || i == (len - 1)) {
            result[dest] = '0' + vals[i];
            dest++;
        }
    }

    return result;
}

int *alloc_zeroed(int len)
{
    int *buf = malloc(sizeof(int) * len);
    memset(buf, 0, len * sizeof(buf[0]));

    return buf;
}

char *multiply_long(char *str1, char *str2)
{
    int len1 = strlen(str1);
    int len2 = strlen(str2);
    int result_len = len1 + len2;

    int *val1 = numeric_string_to_int_array(str1, len1);
    int *val2 = numeric_string_to_int_array(str2, len2);
    int *result = alloc_zeroed(result_len);

    for (int i = len1 - 1; i >= 0; i--) {
        for (int j = len2 - 1; j >= 0; j--) {
            int result_idx = i + j + 1;

            // Multiply the two digits and break out the components.
            int product = val1[i] * val2[j];
            int digit = product % 10;
            int initial_carry = product / 10;

            // Update the result array in-place. The update might force a
            // cell to roll over (10+), triggering the need to factor this
            // calculation into the carry.
            result[result_idx] += digit;
            int extra_carry = result[result_idx] / 10;

            // Perform final updates (reducing the target cell to be < 10
            // and adding in the carry).
            result[result_idx] %= 10;
            result[result_idx - 1] += (initial_carry + extra_carry);
        }
    }

    free(val1);
    free(val2);

    char *result_str = int_array_to_numeric_string(result, result_len);
    free(result);

    return result_str;
}

char *multiply_recursive(char *str1, char *str2)
{
    int len1 = strlen(str1);
    int len2 = strlen(str2);
    int result_len = len1 + len2;

    int *result = alloc_zeroed(result_len);
    char *result_str = int_array_to_numeric_string(result, result_len);
    free(result);

    return result_str;
}