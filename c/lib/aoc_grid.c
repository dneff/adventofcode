#define _POSIX_C_SOURCE 200809L

#include "aoc_grid.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

Grid *grid_new(char **lines, size_t num_lines) {
    if (lines == NULL || num_lines == 0) return NULL;

    Grid *grid = malloc(sizeof(Grid));
    if (grid == NULL) return NULL;

    grid->height = (int)num_lines;
    grid->width = (int)strlen(lines[0]);

    /* Allocate rows */
    grid->cells = malloc(grid->height * sizeof(char *));
    if (grid->cells == NULL) {
        free(grid);
        return NULL;
    }

    /* Copy each row */
    for (int y = 0; y < grid->height; y++) {
        grid->cells[y] = strdup(lines[y]);
        if (grid->cells[y] == NULL) {
            /* Clean up on error */
            for (int i = 0; i < y; i++) {
                free(grid->cells[i]);
            }
            free(grid->cells);
            free(grid);
            return NULL;
        }
    }

    return grid;
}

Grid *grid_new_empty(int width, int height, char fill_char) {
    if (width <= 0 || height <= 0) return NULL;

    Grid *grid = malloc(sizeof(Grid));
    if (grid == NULL) return NULL;

    grid->width = width;
    grid->height = height;

    grid->cells = malloc(height * sizeof(char *));
    if (grid->cells == NULL) {
        free(grid);
        return NULL;
    }

    for (int y = 0; y < height; y++) {
        grid->cells[y] = malloc((width + 1) * sizeof(char));
        if (grid->cells[y] == NULL) {
            for (int i = 0; i < y; i++) {
                free(grid->cells[i]);
            }
            free(grid->cells);
            free(grid);
            return NULL;
        }
        memset(grid->cells[y], fill_char, width);
        grid->cells[y][width] = '\0';
    }

    return grid;
}

void grid_free(Grid *grid) {
    if (grid == NULL) return;

    for (int y = 0; y < grid->height; y++) {
        free(grid->cells[y]);
    }
    free(grid->cells);
    free(grid);
}

char grid_get(const Grid *grid, Point p) {
    if (!grid_in_bounds(grid, p)) return '\0';
    return grid->cells[p.y][p.x];
}

bool grid_set(Grid *grid, Point p, char c) {
    if (!grid_in_bounds(grid, p)) return false;
    grid->cells[p.y][p.x] = c;
    return true;
}

bool grid_in_bounds(const Grid *grid, Point p) {
    return p.x >= 0 && p.x < grid->width && p.y >= 0 && p.y < grid->height;
}

bool grid_find(const Grid *grid, char c, Point *result) {
    for (int y = 0; y < grid->height; y++) {
        for (int x = 0; x < grid->width; x++) {
            if (grid->cells[y][x] == c) {
                *result = point_new(x, y);
                return true;
            }
        }
    }
    return false;
}

Point *grid_find_all(const Grid *grid, char c, size_t *count) {
    *count = 0;
    size_t capacity = 16;
    Point *points = malloc(capacity * sizeof(Point));
    if (points == NULL) return NULL;

    for (int y = 0; y < grid->height; y++) {
        for (int x = 0; x < grid->width; x++) {
            if (grid->cells[y][x] == c) {
                if (*count >= capacity) {
                    capacity *= 2;
                    Point *new_points = realloc(points, capacity * sizeof(Point));
                    if (new_points == NULL) {
                        free(points);
                        *count = 0;
                        return NULL;
                    }
                    points = new_points;
                }
                points[(*count)++] = point_new(x, y);
            }
        }
    }

    return points;
}

int grid_neighbors4(const Grid *grid, Point p, Point *neighbors) {
    Point all_neighbors[4];
    point_neighbors4(p, all_neighbors);

    int count = 0;
    for (int i = 0; i < 4; i++) {
        if (grid_in_bounds(grid, all_neighbors[i])) {
            neighbors[count++] = all_neighbors[i];
        }
    }

    return count;
}

int grid_neighbors8(const Grid *grid, Point p, Point *neighbors) {
    Point all_neighbors[8];
    point_neighbors8(p, all_neighbors);

    int count = 0;
    for (int i = 0; i < 8; i++) {
        if (grid_in_bounds(grid, all_neighbors[i])) {
            neighbors[count++] = all_neighbors[i];
        }
    }

    return count;
}

void grid_print(const Grid *grid) {
    for (int y = 0; y < grid->height; y++) {
        printf("%s\n", grid->cells[y]);
    }
}

int grid_count(const Grid *grid, char c) {
    int count = 0;
    for (int y = 0; y < grid->height; y++) {
        for (int x = 0; x < grid->width; x++) {
            if (grid->cells[y][x] == c) {
                count++;
            }
        }
    }
    return count;
}
