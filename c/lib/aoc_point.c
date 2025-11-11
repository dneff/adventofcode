#include "aoc_point.h"
#include <stdlib.h>

/* Direction constants */
const Point NORTH = {0, -1};
const Point SOUTH = {0, 1};
const Point EAST = {1, 0};
const Point WEST = {-1, 0};
const Point NORTHEAST = {1, -1};
const Point NORTHWEST = {-1, -1};
const Point SOUTHEAST = {1, 1};
const Point SOUTHWEST = {-1, 1};

Point point_new(int x, int y) {
    Point p = {x, y};
    return p;
}

Point point_add(Point a, Point b) {
    Point p = {a.x + b.x, a.y + b.y};
    return p;
}

Point point_sub(Point a, Point b) {
    Point p = {a.x - b.x, a.y - b.y};
    return p;
}

Point point_mul(Point p, int scalar) {
    Point result = {p.x * scalar, p.y * scalar};
    return result;
}

bool point_equal(Point a, Point b) {
    return a.x == b.x && a.y == b.y;
}

int point_manhattan_distance(Point a, Point b) {
    return abs(a.x - b.x) + abs(a.y - b.y);
}

int point_neighbors4(Point p, Point *neighbors) {
    neighbors[0] = point_add(p, NORTH);
    neighbors[1] = point_add(p, SOUTH);
    neighbors[2] = point_add(p, EAST);
    neighbors[3] = point_add(p, WEST);
    return 4;
}

int point_neighbors8(Point p, Point *neighbors) {
    neighbors[0] = point_add(p, NORTH);
    neighbors[1] = point_add(p, SOUTH);
    neighbors[2] = point_add(p, EAST);
    neighbors[3] = point_add(p, WEST);
    neighbors[4] = point_add(p, NORTHEAST);
    neighbors[5] = point_add(p, NORTHWEST);
    neighbors[6] = point_add(p, SOUTHEAST);
    neighbors[7] = point_add(p, SOUTHWEST);
    return 8;
}

Point point_turn_right(Point dir) {
    /* Rotate 90 degrees clockwise: (x, y) -> (y, -x) */
    Point p = {-dir.y, dir.x};
    return p;
}

Point point_turn_left(Point dir) {
    /* Rotate 90 degrees counter-clockwise: (x, y) -> (-y, x) */
    Point p = {dir.y, -dir.x};
    return p;
}

Point point_from_direction_char(char c) {
    switch (c) {
        case 'N': case 'U': case '^':
            return NORTH;
        case 'S': case 'D': case 'v':
            return SOUTH;
        case 'E': case 'R': case '>':
            return EAST;
        case 'W': case 'L': case '<':
            return WEST;
        default:
            return point_new(0, 0);
    }
}

unsigned long point_hash(Point p) {
    /* Simple hash function combining x and y coordinates */
    unsigned long hash = 17;
    hash = hash * 31 + (unsigned long)p.x;
    hash = hash * 31 + (unsigned long)p.y;
    return hash;
}
