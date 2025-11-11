#ifndef AOC_POINT_H
#define AOC_POINT_H

#include <stdbool.h>
#include <stddef.h>

/**
 * 2D point structure.
 */
typedef struct {
    int x;
    int y;
} Point;

/**
 * Direction vectors (cardinal directions).
 */
extern const Point NORTH;
extern const Point SOUTH;
extern const Point EAST;
extern const Point WEST;

/**
 * Diagonal direction vectors.
 */
extern const Point NORTHEAST;
extern const Point NORTHWEST;
extern const Point SOUTHEAST;
extern const Point SOUTHWEST;

/**
 * Create a new point.
 * @param x X coordinate
 * @param y Y coordinate
 * @return New point
 */
Point point_new(int x, int y);

/**
 * Add two points.
 * @param a First point
 * @param b Second point
 * @return Sum of the points
 */
Point point_add(Point a, Point b);

/**
 * Subtract two points.
 * @param a First point
 * @param b Second point
 * @return Difference of the points
 */
Point point_sub(Point a, Point b);

/**
 * Multiply a point by a scalar.
 * @param p Point
 * @param scalar Scalar value
 * @return Scaled point
 */
Point point_mul(Point p, int scalar);

/**
 * Check if two points are equal.
 * @param a First point
 * @param b Second point
 * @return true if equal, false otherwise
 */
bool point_equal(Point a, Point b);

/**
 * Calculate Manhattan distance between two points.
 * @param a First point
 * @param b Second point
 * @return Manhattan distance
 */
int point_manhattan_distance(Point a, Point b);

/**
 * Get the 4 orthogonally adjacent neighbors of a point.
 * @param p The point
 * @param neighbors Output array (must have space for 4 points)
 * @return Number of neighbors (always 4)
 */
int point_neighbors4(Point p, Point *neighbors);

/**
 * Get the 8 neighbors (including diagonals) of a point.
 * @param p The point
 * @param neighbors Output array (must have space for 8 points)
 * @return Number of neighbors (always 8)
 */
int point_neighbors8(Point p, Point *neighbors);

/**
 * Turn a direction vector 90 degrees right (clockwise).
 * @param dir Direction vector
 * @return New direction vector
 */
Point point_turn_right(Point dir);

/**
 * Turn a direction vector 90 degrees left (counter-clockwise).
 * @param dir Direction vector
 * @return New direction vector
 */
Point point_turn_left(Point dir);

/**
 * Convert a direction character to a direction vector.
 * @param c Direction character (N, S, E, W, U, D, L, R, ^, v, <, >)
 * @return Direction vector
 */
Point point_from_direction_char(char c);

/**
 * Hash function for a point (useful for hash tables).
 * @param p The point
 * @return Hash value
 */
unsigned long point_hash(Point p);

#endif /* AOC_POINT_H */
