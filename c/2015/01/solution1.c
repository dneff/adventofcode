/*
 * Advent of Code 2015 - Day 1: Not Quite Lisp
 * Part 1: Find the floor Santa ends up on
 * https://adventofcode.com/2015/day/1
 */

#include "../../lib/aoc_input.h"
#include "../../lib/aoc_utils.h"
#include <stdlib.h>
#include <string.h>

int solve_part1(const char *input) {
    int floor = 0;

    for (size_t i = 0; i < strlen(input); i++) {
        if (input[i] == '(') {
            floor++;
        } else if (input[i] == ')') {
            floor--;
        }
    }

    return floor;
}

int main(void) {
    char input_path[256];
    get_input_path(2015, 1, input_path, sizeof(input_path));

    char *input = read_file(input_path);
    if (input == NULL) {
        return 1;
    }

    int answer = solve_part1(input);
    print_solution_int(1, answer);

    free(input);
    return 0;
}
