/*
 * Advent of Code 2015 - Day 1: Not Quite Lisp
 * Part 2: Find the position where Santa first enters the basement (floor -1)
 * https://adventofcode.com/2015/day/1
 */

#include "../../lib/aoc_input.h"
#include "../../lib/aoc_utils.h"
#include <stdlib.h>
#include <string.h>

int solve_part2(const char *input) {
    int floor = 0;

    for (size_t i = 0; i < strlen(input); i++) {
        if (input[i] == '(') {
            floor++;
        } else if (input[i] == ')') {
            floor--;
        }

        if (floor == -1) {
            return (int)(i + 1);  /* Position is 1-indexed */
        }
    }

    return -1;  /* Never entered basement */
}

int main(void) {
    char input_path[256];
    get_input_path(2015, 1, input_path, sizeof(input_path));

    char *input = read_file(input_path);
    if (input == NULL) {
        return 1;
    }

    int answer = solve_part2(input);
    print_solution_int(2, answer);

    free(input);
    return 0;
}
