#ifndef AOC_GRID_H
#define AOC_GRID_H

#include "aoc_point.h"
#include <stddef.h>
#include <stdbool.h>

/**
 * 2D grid structure (stored as a 2D array).
 */
typedef struct {
    char **cells;    /* 2D array of characters */
    int width;       /* Width of the grid */
    int height;      /* Height of the grid */
} Grid;

/**
 * Create a new grid from an array of strings.
 * @param lines Array of strings (rows)
 * @param num_lines Number of lines
 * @return New grid
 * @note Caller must free the grid using grid_free()
 */
Grid *grid_new(char **lines, size_t num_lines);

/**
 * Create an empty grid with specified dimensions.
 * @param width Width of the grid
 * @param height Height of the grid
 * @param fill_char Character to fill the grid with
 * @return New grid
 * @note Caller must free the grid using grid_free()
 */
Grid *grid_new_empty(int width, int height, char fill_char);

/**
 * Free a grid.
 * @param grid The grid to free
 */
void grid_free(Grid *grid);

/**
 * Get a character at a specific position.
 * @param grid The grid
 * @param p The position
 * @return Character at the position, or '\0' if out of bounds
 */
char grid_get(const Grid *grid, Point p);

/**
 * Set a character at a specific position.
 * @param grid The grid
 * @param p The position
 * @param c The character to set
 * @return true if successful, false if out of bounds
 */
bool grid_set(Grid *grid, Point p, char c);

/**
 * Check if a position is within the grid bounds.
 * @param grid The grid
 * @param p The position
 * @return true if in bounds, false otherwise
 */
bool grid_in_bounds(const Grid *grid, Point p);

/**
 * Find the first occurrence of a character in the grid.
 * @param grid The grid
 * @param c The character to find
 * @param result Pointer to store the result
 * @return true if found, false otherwise
 */
bool grid_find(const Grid *grid, char c, Point *result);

/**
 * Find all occurrences of a character in the grid.
 * @param grid The grid
 * @param c The character to find
 * @param count Pointer to store the count
 * @return Array of points where the character was found
 * @note Caller must free the returned array
 */
Point *grid_find_all(const Grid *grid, char c, size_t *count);

/**
 * Get the 4 orthogonally adjacent neighbors that are in bounds.
 * @param grid The grid
 * @param p The position
 * @param neighbors Output array (must have space for 4 points)
 * @return Number of neighbors in bounds
 */
int grid_neighbors4(const Grid *grid, Point p, Point *neighbors);

/**
 * Get the 8 neighbors (including diagonals) that are in bounds.
 * @param grid The grid
 * @param p The position
 * @param neighbors Output array (must have space for 8 points)
 * @return Number of neighbors in bounds
 */
int grid_neighbors8(const Grid *grid, Point p, Point *neighbors);

/**
 * Print the grid to stdout.
 * @param grid The grid
 */
void grid_print(const Grid *grid);

/**
 * Count occurrences of a character in the grid.
 * @param grid The grid
 * @param c The character to count
 * @return Number of occurrences
 */
int grid_count(const Grid *grid, char c);

#endif /* AOC_GRID_H */
