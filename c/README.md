# C Solutions for Advent of Code

This directory contains C implementations of Advent of Code solutions, featuring a comprehensive helper library for common operations like input parsing, grid manipulation, pathfinding, and mathematical utilities.

## Requirements

- GCC or Clang compiler (C11 standard)
- Make build system
- Standard C library with POSIX extensions

### Installing Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get install build-essential
```

**macOS:**
```bash
xcode-select --install
# or
brew install gcc make
```

**Fedora/RHEL:**
```bash
sudo dnf install gcc make
```

## Directory Structure

```
c/
├── README.md              # This file
├── Makefile               # Main build system
├── verify_solutions.c     # Solution verification program
├── lib/                   # Helper library
│   ├── aoc_input.h        # Input reading and parsing
│   ├── aoc_input.c
│   ├── aoc_point.h        # 2D point operations
│   ├── aoc_point.c
│   ├── aoc_grid.h         # 2D grid operations
│   ├── aoc_grid.c
│   ├── aoc_math.h         # Mathematical utilities
│   ├── aoc_math.c
│   ├── aoc_utils.h        # Common utility functions
│   └── aoc_utils.c
└── 2015/                  # Year-organized solutions
    ├── 01/
    │   ├── solution1.c
    │   ├── solution2.c
    │   └── Makefile
    └── ...
```

## Building and Running Solutions

### Building the Helper Library

From the `c/` directory:
```bash
make lib
```

### Building and Running Individual Solutions

```bash
# Navigate to the solution directory
cd 2015/01

# Build both parts
make

# Run the solutions
./solution1
./solution2

# Or build and run in one step
make run
```

### Building the Verification Script

```bash
# From the c/ directory
make verify
```

## Helper Library Usage

The helper library provides reusable modules for common Advent of Code tasks.

### Input Module (`aoc_input.h`)

Reading and parsing input files:

```c
#include "../../lib/aoc_input.h"

/* Read all lines from a file */
LineArray lines = read_lines("input.txt");
for (size_t i = 0; i < lines.count; i++) {
    printf("%s\n", lines.lines[i]);
}
free_line_array(&lines);

/* Read entire file as a string */
char *content = read_file("input.txt");
/* ... use content ... */
free(content);

/* Read all integers (one per line) */
IntArray numbers = read_numbers("input.txt");
for (size_t i = 0; i < numbers.count; i++) {
    printf("%d\n", numbers.numbers[i]);
}
free_int_array(&numbers);

/* Parse all numbers from text */
size_t count;
int *nums = parse_numbers("move 5 from 3 to 7", &count);
/* nums = [5, 3, 7], count = 3 */
free(nums);

/* Get input path for aoc-data structure */
char path[256];
get_input_path(2015, 1, path, sizeof(path));
/* path = "../../../aoc-data/2015/1/input" */
```

### Point Module (`aoc_point.h`)

2D coordinate handling:

```c
#include "../../lib/aoc_point.h"

/* Create points */
Point p1 = point_new(3, 4);
Point p2 = point_new(1, 2);

/* Arithmetic operations */
Point p3 = point_add(p1, p2);        /* (4, 6) */
Point p4 = point_sub(p1, p2);        /* (2, 2) */
Point p5 = point_mul(p1, 2);         /* (6, 8) */

/* Comparison */
if (point_equal(p1, p2)) {
    printf("Points are equal\n");
}

/* Distance */
int dist = point_manhattan_distance(p1, p2);  /* 4 */

/* Direction constants */
Point next = point_add(p1, NORTH);   /* Move up */
next = point_add(p1, EAST);          /* Move right */

/* Get neighbors */
Point neighbors[4];
int count = point_neighbors4(p1, neighbors);  /* 4 orthogonal neighbors */

Point all_neighbors[8];
count = point_neighbors8(p1, all_neighbors);  /* 8 including diagonals */

/* Turn directions */
Point new_dir = point_turn_right(NORTH);  /* EAST */
new_dir = point_turn_left(NORTH);         /* WEST */

/* Convert from direction character */
Point dir = point_from_direction_char('^');  /* NORTH */
```

### Grid Module (`aoc_grid.h`)

2D grid operations:

```c
#include "../../lib/aoc_grid.h"

/* Create grid from lines */
LineArray lines = read_lines("input.txt");
Grid *grid = grid_new(lines.lines, lines.count);
free_line_array(&lines);

/* Create empty grid */
Grid *grid2 = grid_new_empty(10, 10, '.');

/* Access grid cells */
Point p = point_new(3, 4);
char value = grid_get(grid, p);
grid_set(grid, p, 'X');

/* Check bounds */
if (grid_in_bounds(grid, p)) {
    printf("Point is in bounds\n");
}

/* Find values */
Point start;
if (grid_find(grid, 'S', &start)) {
    printf("Found 'S' at (%d, %d)\n", start.x, start.y);
}

size_t count;
Point *positions = grid_find_all(grid, '#', &count);
/* ... use positions ... */
free(positions);

/* Get neighbors */
Point neighbors[4];
int n = grid_neighbors4(grid, p, neighbors);  /* In-bounds neighbors */

Point all_neighbors[8];
n = grid_neighbors8(grid, p, all_neighbors);

/* Print grid */
grid_print(grid);

/* Count occurrences */
int wall_count = grid_count(grid, '#');

/* Clean up */
grid_free(grid);
```

### Math Module (`aoc_math.h`)

Mathematical utilities:

```c
#include "../../lib/aoc_math.h"

/* GCD and LCM */
long long g = gcd(48, 18);                  /* 6 */
long long l = lcm(12, 18);                  /* 36 */

long long numbers[] = {48, 18, 24};
g = gcd_array(numbers, 3);                  /* 6 */
l = lcm_array(numbers, 3);                  /* 144 */

/* Primes */
if (is_prime(17)) {
    printf("17 is prime\n");
}

size_t count;
int *primes = primes_up_to(100, &count);
/* primes = [2, 3, 5, 7, 11, ...] */
free(primes);

/* Factorization */
size_t factor_count;
long long *factors = prime_factors(60, &factor_count);
/* factors = [2, 2, 3, 5] */
free(factors);

long long *divs = divisors(12, &count);
/* divs = [1, 2, 3, 4, 6, 12] */
free(divs);

/* Combinatorics */
long long fact = factorial(5);              /* 120 */
long long comb = binomial(5, 2);            /* 10 */

/* Power functions */
long long p = power(2, 10);                 /* 1024 */
long long mp = mod_power(2, 10, 1000);      /* 24 */
```

### Utils Module (`aoc_utils.h`)

Common utility functions:

```c
#include "../../lib/aoc_utils.h"

/* Print solutions */
print_solution_int(1, 42);                  /* "Part 1: 42" */
print_solution(2, "answer");                /* "Part 2: answer" */

/* Array operations */
int arr[] = {1, 5, 3, 8, 2};
long long total = sum(arr, 5);              /* 19 */
long long prod = product(arr, 5);           /* 240 */
int min = min_value(arr, 5);                /* 1 */
int max = max_value(arr, 5);                /* 8 */

/* Counting with predicate */
bool is_positive(int x) { return x > 0; }
int count = count_if(arr, 5, is_positive);  /* 5 */

/* String utilities */
char str[] = "  hello  ";
char *trimmed = trim(str);                  /* "hello" */

/* Number utilities */
int s = sign(-5);                           /* -1 */
int c = clamp(15, 0, 10);                   /* 10 */

/* Binary conversion */
long long dec = binary_to_decimal("1010");  /* 10 */
```

## Solution Template

Here's a typical solution structure:

```c
/*
 * Advent of Code 2015 - Day 1: Not Quite Lisp
 * https://adventofcode.com/2015/day/1
 */

#include "../../lib/aoc_input.h"
#include "../../lib/aoc_utils.h"
#include <stdlib.h>

int solve_part1(const char *input) {
    /* Solution logic here */
    int answer = 0;
    return answer;
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
```

## Verifying Solutions

Use the verification script to check solutions against known answers:

```bash
# Build the verification script first
make verify

# Verify all solutions
./verify_solutions

# Verify specific year
./verify_solutions 2015

# Verify specific day
./verify_solutions 2015 1

# Write missing answers to aoc-data
./verify_solutions --write-missing
./verify_solutions 2015 --write-missing
```

The verification script:
- Automatically builds solutions using their Makefiles
- Runs each solution and captures output
- Compares against answers in `aoc-data` repository
- Shows colored output with timing information
- Supports writing missing answers for new solutions

## Memory Management

The C helper library uses dynamic memory allocation for flexibility. Always remember to:

1. Free `LineArray` structures with `free_line_array()`
2. Free `IntArray` structures with `free_int_array()`
3. Free `Grid` structures with `grid_free()`
4. Free strings returned by `read_file()`
5. Free arrays returned by functions like `parse_numbers()`, `primes_up_to()`, etc.

Example:
```c
LineArray lines = read_lines("input.txt");
/* ... use lines ... */
free_line_array(&lines);  /* Always free when done */
```

## Compiler Flags

Solutions are compiled with:
- `-Wall -Wextra`: Enable all warnings
- `-std=c11`: Use C11 standard
- `-O2`: Optimization level 2
- `-I./lib`: Include helper library headers
- `-lm`: Link math library

## Input Files

Solutions expect input files at:
```
../../../aoc-data/YEAR/DAY/input
```

This path is relative to each solution executable. The `get_input_path()` function automatically handles this path resolution.

## Common Patterns

### Reading and Processing Lines
```c
LineArray lines = read_lines(input_path);
for (size_t i = 0; i < lines.count; i++) {
    /* Process each line */
    printf("%s\n", lines.lines[i]);
}
free_line_array(&lines);
```

### Grid Traversal with BFS
```c
Grid *grid = /* ... create grid ... */;
Point start;
grid_find(grid, 'S', &start);

/* Simple BFS implementation */
Point queue[10000];
int visited[1000][1000] = {0};
int front = 0, back = 0;

queue[back++] = start;
visited[start.y][start.x] = 1;

while (front < back) {
    Point current = queue[front++];

    Point neighbors[4];
    int count = grid_neighbors4(grid, current, neighbors);

    for (int i = 0; i < count; i++) {
        Point next = neighbors[i];
        if (!visited[next.y][next.x] && grid_get(grid, next) != '#') {
            visited[next.y][next.x] = 1;
            queue[back++] = next;
        }
    }
}
```

### Number Parsing
```c
char *line = "move 5 from 3 to 7";
size_t count;
int *numbers = parse_numbers(line, &count);
/* numbers = [5, 3, 7], count = 3 */

/* Use the numbers */
for (size_t i = 0; i < count; i++) {
    printf("%d ", numbers[i]);
}

free(numbers);
```

## Tips

1. **Memory Management**: Always free allocated memory to prevent leaks
2. **Error Checking**: Check return values from functions that can fail
3. **Grid Coordinates**: The library uses (x, y) coordinates where x is the column and y is the row
4. **Array Bounds**: Helper functions like `grid_neighbors4()` automatically filter out-of-bounds positions
5. **Performance**: The library is designed for clarity; optimize hot paths as needed
6. **Debugging**: Use `grid_print()` to visualize grid state during development

## Resources

- [C11 Standard Documentation](https://en.cppreference.com/w/c)
- [GCC Manual](https://gcc.gnu.org/onlinedocs/gcc/)
- [Make Manual](https://www.gnu.org/software/make/manual/)
- [Advent of Code](https://adventofcode.com/)

## Author

Advent of Code Solutions Collection
