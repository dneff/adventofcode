#include "aoc_utils.h"
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <limits.h>

void print_solution(int part, const char *answer) {
    printf("Part %d: %s\n", part, answer);
}

void print_solution_int(int part, long long answer) {
    printf("Part %d: %lld\n", part, answer);
}

char *trim(char *str) {
    if (str == NULL) return NULL;

    /* Trim leading whitespace */
    while (isspace((unsigned char)*str)) str++;

    if (*str == 0) return str;

    /* Trim trailing whitespace */
    char *end = str + strlen(str) - 1;
    while (end > str && isspace((unsigned char)*end)) end--;

    /* Write new null terminator */
    end[1] = '\0';

    return str;
}

int count_if(const int *array, size_t size, bool (*predicate)(int)) {
    int count = 0;
    for (size_t i = 0; i < size; i++) {
        if (predicate(array[i])) {
            count++;
        }
    }
    return count;
}

long long sum(const int *array, size_t size) {
    long long total = 0;
    for (size_t i = 0; i < size; i++) {
        total += array[i];
    }
    return total;
}

long long product(const int *array, size_t size) {
    long long result = 1;
    for (size_t i = 0; i < size; i++) {
        result *= array[i];
    }
    return result;
}

int min_value(const int *array, size_t size) {
    if (size == 0) return INT_MAX;

    int min = array[0];
    for (size_t i = 1; i < size; i++) {
        if (array[i] < min) {
            min = array[i];
        }
    }
    return min;
}

int max_value(const int *array, size_t size) {
    if (size == 0) return INT_MIN;

    int max = array[0];
    for (size_t i = 1; i < size; i++) {
        if (array[i] > max) {
            max = array[i];
        }
    }
    return max;
}

long long binary_to_decimal(const char *binary) {
    long long result = 0;
    while (*binary) {
        result = (result << 1) | (*binary == '1' ? 1 : 0);
        binary++;
    }
    return result;
}

int sign(int x) {
    return (x > 0) - (x < 0);
}

int clamp(int value, int min, int max) {
    if (value < min) return min;
    if (value > max) return max;
    return value;
}
