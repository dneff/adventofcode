#ifndef AOC_INPUT_H
#define AOC_INPUT_H

#include <stddef.h>

/**
 * Structure to hold lines read from a file.
 */
typedef struct {
    char **lines;    /* Array of strings */
    size_t count;    /* Number of lines */
} LineArray;

/**
 * Structure to hold integers read from a file.
 */
typedef struct {
    int *numbers;    /* Array of integers */
    size_t count;    /* Number of integers */
} IntArray;

/**
 * Read all lines from a file.
 * @param filename Path to the file
 * @return LineArray structure with lines and count
 * @note Caller must free the returned structure using free_line_array()
 */
LineArray read_lines(const char *filename);

/**
 * Read entire file as a single string.
 * @param filename Path to the file
 * @return File contents as a string
 * @note Caller must free the returned string
 */
char *read_file(const char *filename);

/**
 * Read all integers from a file (one per line).
 * @param filename Path to the file
 * @return IntArray structure with numbers and count
 * @note Caller must free the returned structure using free_int_array()
 */
IntArray read_numbers(const char *filename);

/**
 * Parse all integers from a string (supports negative numbers).
 * @param text The text to parse
 * @param count Pointer to store the count of numbers found
 * @return Array of integers
 * @note Caller must free the returned array
 */
int *parse_numbers(const char *text, size_t *count);

/**
 * Free a LineArray structure.
 * @param arr The LineArray to free
 */
void free_line_array(LineArray *arr);

/**
 * Free an IntArray structure.
 * @param arr The IntArray to free
 */
void free_int_array(IntArray *arr);

/**
 * Get the input file path (resolves relative paths to aoc-data).
 * @param year The year (e.g., 2015)
 * @param day The day (1-25)
 * @param buffer Buffer to store the path
 * @param buffer_size Size of the buffer
 * @return Pointer to the buffer
 */
char *get_input_path(int year, int day, char *buffer, size_t buffer_size);

#endif /* AOC_INPUT_H */
