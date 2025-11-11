#ifndef AOC_UTILS_H
#define AOC_UTILS_H

#include <stddef.h>
#include <stdbool.h>

/**
 * Print solution result in standard format.
 * @param part The part number (1 or 2)
 * @param answer The answer as a string
 */
void print_solution(int part, const char *answer);

/**
 * Print solution result (integer version).
 * @param part The part number (1 or 2)
 * @param answer The answer as an integer
 */
void print_solution_int(int part, long long answer);

/**
 * Trim whitespace from the beginning and end of a string (in place).
 * @param str The string to trim
 * @return Pointer to the trimmed string
 */
char *trim(char *str);

/**
 * Count elements in an array that satisfy a predicate.
 * @param array Array of integers
 * @param size Size of the array
 * @param predicate Function that returns true for elements to count
 * @return Number of elements satisfying the predicate
 */
int count_if(const int *array, size_t size, bool (*predicate)(int));

/**
 * Sum all elements in an integer array.
 * @param array Array of integers
 * @param size Size of the array
 * @return Sum of all elements
 */
long long sum(const int *array, size_t size);

/**
 * Find the product of all elements in an integer array.
 * @param array Array of integers
 * @param size Size of the array
 * @return Product of all elements
 */
long long product(const int *array, size_t size);

/**
 * Find minimum value in an integer array.
 * @param array Array of integers
 * @param size Size of the array
 * @return Minimum value
 */
int min_value(const int *array, size_t size);

/**
 * Find maximum value in an integer array.
 * @param array Array of integers
 * @param size Size of the array
 * @return Maximum value
 */
int max_value(const int *array, size_t size);

/**
 * Convert binary string to decimal integer.
 * @param binary Binary string (e.g., "1010")
 * @return Decimal value
 */
long long binary_to_decimal(const char *binary);

/**
 * Get the sign of a number.
 * @param x The number
 * @return -1, 0, or 1
 */
int sign(int x);

/**
 * Clamp a value between min and max.
 * @param value The value to clamp
 * @param min Minimum value
 * @param max Maximum value
 * @return Clamped value
 */
int clamp(int value, int min, int max);

#endif /* AOC_UTILS_H */
