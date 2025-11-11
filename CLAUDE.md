# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Structure

This is an Advent of Code solutions repository organized by language and year:

```
adventofcode/
├── python/           # Python solutions (2015-2024)
│   ├── YEAR/DAY/    # solution1.py, solution2.py
│   ├── aoc_helpers.py   # Comprehensive helper library
│   ├── verify_solutions.py    # Verification script
│   ├── refactor_solutions.py  # Refactoring utility
│   └── input/       # Input files (some years)
├── javascript/      # JavaScript solutions (2015)
│   ├── YEAR/DAY/    # solution1.js, solution2.js
│   ├── aoc-helpers.js       # Comprehensive helper library
│   ├── verify_solutions.js  # Verification script
│   └── package.json # npm configuration
├── go/              # Go solutions (2015, 2022)
│   ├── pkg/         # Helper library packages
│   ├── YEAR/DAY/    # solution1.go, solution2.go
│   ├── verify_solutions.go  # Verification tool
│   ├── go.mod       # Module definition
│   └── README.md    # Go documentation
├── c/               # C solutions (2015)
│   ├── lib/         # Helper library modules
│   ├── verify_solutions.c  # Verification program
│   └── YEAR/DAY/    # solution1.c, solution2.c, Makefile
├── clojure/         # Clojure solutions (2015)
│   ├── src/aoc/     # Helper library namespaces
│   ├── verify_solutions.clj  # Verification script
│   ├── deps.edn     # Dependency configuration
│   └── yearYYYY/    # Year-organized solutions
│       └── dayDD.clj # Namespace with solve-part1, solve-part2
├── scheme/          # Racket/Scheme solutions (2015)
│   ├── helpers/     # Helper library modules
│   └── 2015/        # Year-organized solutions
│       └── DAY/     # solution1.rkt, solution2.rkt
└── perl/            # Perl solutions (2015)
    ├── lib/AoC/     # Helper modules
    ├── verify_solutions.pl  # Verification script
    └── 2015/        # Year-organized solutions
        └── DAY/     # solution1.pl, solution2.pl
```

**Design Principle**: The root directory contains only documentation and configuration files (*.md, *.txt, *.yaml, etc.). All language-specific code, including utility scripts and tooling, resides within language-specific subdirectories (e.g., `python/`, `go/`). This keeps the repository root clean and makes the multi-language structure immediately apparent.

## Python Development

### Key Files
- `python/aoc_helpers.py`: Comprehensive helper library with utilities for input reading, grid operations, pathfinding, coordinate handling, and mathematical functions
- `python/README.md`: Detailed usage guide for the helper library
- `python/verify_solutions.py`: Script to verify solutions against known correct answers from the `aoc-data` repository
- `python/refactor_solutions.py`: Utility to refactor solution files to use aoc_helpers and aoc-data

### Running Solutions
```bash
# Run from repository root
python python/YEAR/DAY/solution1.py
python python/YEAR/DAY/solution2.py
```

### Code Style
- Linting configured in `python/2015/tox.ini`: flake8 with max line length 119, complexity limit 10
- Use helper library classes: `AoCInput`, `Grid2D`, `Point2D`, `Pathfinding`, `MathUtils`, `Directions`, `AoCUtils`

### Helper Library Usage
Most solutions should leverage the helper library for common operations:
- Input reading: `AoCInput.read_lines()`, `AoCInput.read_grid()`, `AoCInput.parse_numbers()`
- Grid operations: `Grid2D` class with adjacency, pathfinding, and position utilities
- Pathfinding: BFS and Dijkstra implementations in `Pathfinding` class
- Mathematical utilities: GCD, LCM, Manhattan distance in `MathUtils`

## JavaScript Development

### Key Files
- `javascript/aoc-helpers.js`: Comprehensive helper library with utilities for input reading, grid operations, pathfinding, coordinate handling, and mathematical functions
- `javascript/README.md`: Detailed usage guide for the helper library
- `javascript/verify_solutions.js`: Script to verify solutions against known correct answers from the `aoc-data` repository
- `javascript/package.json`: npm configuration with scripts for testing, linting, and verification

### Running Solutions
```bash
# Run from repository root
node javascript/YEAR/DAY/solution1.js
node javascript/YEAR/DAY/solution2.js
```

### Code Style
- ES6 modules (`import`/`export`)
- ESLint configured with ES2024 features
- Maximum line length: 120 characters
- Maximum complexity: 15
- Use helper library classes: `AoCInput`, `Grid2D`, `Point2D`, `Pathfinding`, `MathUtils`, `Directions`, `AoCUtils`

### Helper Library Usage
Most solutions should leverage the helper library for common operations:
- Input reading: `AoCInput.readLines()`, `AoCInput.readGrid()`, `AoCInput.parseNumbers()`
- Grid operations: `Grid2D` class with adjacency, pathfinding, and position utilities
- Pathfinding: BFS and Dijkstra implementations in `Pathfinding` class
- Mathematical utilities: GCD, LCM, Manhattan distance in `MathUtils`

## Go Development

### Key Files
- `go/pkg/input/`: File reading and parsing utilities
- `go/pkg/point/`: 2D point operations and direction constants
- `go/pkg/grid/`: Generic Grid[T] type with operations
- `go/pkg/math/`: Mathematical utilities (GCD, LCM, primes, etc.)
- `go/pkg/pathfinding/`: BFS and Dijkstra implementations
- `go/pkg/utils/`: Common patterns and formatting utilities
- `go/verify_solutions.go`: Verification tool to test solutions
- `go/README.md`: Comprehensive usage guide for the helper library
- `go/go.mod`: Module definition (Go 1.22+)

### Structure
- Module name: `github.com/dneff/adventofcode/go`
- Go version: 1.22+
- Helper packages: Modular sub-packages under `go/pkg/`

### Running Solutions
```bash
# Run from repository root or go/ directory
cd go/YEAR/DAY
go run solution1.go
go run solution2.go

# Example for 2015 Day 1
cd go/2015/01
go run solution1.go
```

### Code Style
- Go 1.22+ with generics support
- Follow standard Go conventions (`gofmt`, `go vet`)
- Use helper library packages for common operations
- Maximum complexity kept manageable through modular design

### Helper Library Usage
Most solutions should leverage the helper library for common operations:
- Input reading: `input.MustReadLines()`, `input.MustReadFile()`, `input.ParseInts()`, `input.GetInputPath(year, day)`
- Point operations: `point.New(x, y)`, `point.Add()`, `point.Manhattan()`, direction constants (North, South, East, West)
- Grid operations: `grid.New()`, `grid.Get()`, `grid.Set()`, `grid.Neighbors4()`, `grid.Find()`, `grid.Count()`
- Pathfinding: `pathfinding.BFS()`, `pathfinding.Dijkstra()`, `pathfinding.BFSPath()`
- Mathematical utilities: `math.GCD()`, `math.LCM()`, `math.IsPrime()`, `math.PrimesUpTo()`, `math.Combinations()`
- Utility functions: `utils.PrintSolution()`, `utils.Check()`, `utils.Filter()`, `utils.Map()`, `utils.Frequencies()`

## Scheme/Racket Development

### Key Files
- `scheme/helpers/input.rkt`: File I/O and parsing utilities
- `scheme/helpers/point.rkt`: Coordinate handling and direction constants
- `scheme/helpers/grid.rkt`: 2D grid operations
- `scheme/helpers/math.rkt`: Mathematical utilities (GCD, LCM, primes, etc.)
- `scheme/helpers/utils.rkt`: Functional pattern utilities and solution formatting
- `scheme/helpers/pathfinding.rkt`: BFS, Dijkstra, and A* implementations
- `scheme/verify_solutions.rkt`: Verification script to test solutions against known answers
- `scheme/README.md`: Comprehensive usage guide for the helper library

### Running Solutions
```bash
# Run from repository root
racket scheme/YEAR/DAY/solution1.rkt
racket scheme/YEAR/DAY/solution2.rkt
```

### Code Style
- Use functional programming patterns and immutable data structures
- Use helper library modules for common operations
- Keep functions focused and composable
- Use meaningful function and variable names

### Helper Library Usage
Most solutions should leverage the helper library for common operations:
- Input reading: `(read-lines filename)`, `(read-grid filename)`, `(parse-numbers text)`
- Grid operations: `make-grid`, `grid-ref`, `grid-neighbors-4`, `grid-neighbors-8`
- Point operations: `point-add`, `point-neighbors-4`, direction constants (NORTH, SOUTH, EAST, WEST)
- Pathfinding: `bfs`, `dijkstra`, `a-star` implementations
- Mathematical utilities: `gcd`, `lcm`, `primes-up-to`, `factorial`, `combinations`
- Functional utilities: `count-if`, `frequencies`, `group-by`, `memoize`

## C Development

### Key Files
- `c/lib/aoc_input.h/c`: File I/O and parsing utilities
- `c/lib/aoc_point.h/c`: 2D point operations and direction constants
- `c/lib/aoc_grid.h/c`: 2D grid operations
- `c/lib/aoc_math.h/c`: Mathematical utilities (GCD, LCM, primes, etc.)
- `c/lib/aoc_utils.h/c`: Common utility functions
- `c/verify_solutions.c`: Verification program to test solutions against known answers
- `c/README.md`: Comprehensive usage guide for the helper library
- `c/Makefile`: Main build system for library and verification script

### Building and Running Solutions
```bash
# Build from solution directory
cd c/YEAR/DAY
make
./solution1
./solution2

# Or use the run target
make run
```

### Code Style
- C11 standard with GCC/Clang compiler
- Wall -Wextra compiler flags for warnings
- Makefile-based build system
- Manual memory management with proper cleanup

### Helper Library Usage
Most solutions should leverage the helper library for common operations:
- Input reading: `read_lines()`, `read_file()`, `read_numbers()`, `parse_numbers()`
- Point operations: `point_new()`, `point_add()`, `point_neighbors4()`, direction constants (NORTH, SOUTH, EAST, WEST)
- Grid operations: `grid_new()`, `grid_get()`, `grid_set()`, `grid_neighbors4()`, `grid_find()`
- Mathematical utilities: `gcd()`, `lcm()`, `is_prime()`, `primes_up_to()`, `factorial()`
- Utility functions: `sum()`, `product()`, `count_if()`, `print_solution_int()`

## Perl Development

### Key Files
- `perl/lib/AoC/Input.pm`: File I/O and parsing utilities
- `perl/lib/AoC/Point.pm`: 2D point class with operator overloading
- `perl/lib/AoC/Grid.pm`: 2D grid operations
- `perl/lib/AoC/Math.pm`: Mathematical utilities (GCD, LCM, primes, etc.)
- `perl/lib/AoC/Utils.pm`: Common utility functions
- `perl/verify_solutions.pl`: Verification script to test solutions against known answers
- `perl/README.md`: Comprehensive usage guide for the helper library

### Running Solutions
```bash
# Run from repository root
perl perl/YEAR/DAY/solution1.pl
perl perl/YEAR/DAY/solution2.pl
```

### Code Style
- Perl 5.40+ with modern features (subroutine signatures, postfix dereferencing)
- Use `perltidy` for consistent formatting (see `perl/.perltidyrc`)
- Use `perlcritic` for code quality (severity level 3)
- Comprehensive POD documentation in modules

### Helper Library Usage
Most solutions should leverage the helper library for common operations:
- Input reading: `read_lines('input')`, `read_text('input')`, `parse_numbers($text)`
- Point operations: `point($x, $y)`, operator overloading for +/-/*, direction constants (NORTH, SOUTH, EAST, WEST)
- Grid operations: `make_grid(\@rows)`, `grid_get($grid, $point)`, `grid_neighbors4($grid, $point)`
- Mathematical utilities: `gcd($a, $b)`, `lcm($a, $b)`, `primes_up_to($n)`, `factorial($n)`
- Utility functions: `count_if { } @list`, `frequencies(@list)`, `sum(@numbers)`, `product(@numbers)`

## Clojure Development

### Key Files
- `clojure/src/aoc/input.clj`: File I/O and parsing utilities
- `clojure/src/aoc/point.clj`: 2D point operations and direction constants
- `clojure/src/aoc/grid.clj`: 2D grid operations
- `clojure/src/aoc/math.clj`: Mathematical utilities (GCD, LCM, primes, etc.)
- `clojure/src/aoc/pathfinding.clj`: Search algorithms (BFS, Dijkstra, A*)
- `clojure/src/aoc/utils.clj`: General utility functions
- `clojure/verify_solutions.clj`: Verification script to test solutions against known answers
- `clojure/deps.edn`: Dependency configuration
- `clojure/README.md`: Comprehensive usage guide for the helper library

### Running Solutions
```bash
# Run from clojure/ directory
cd clojure
clojure -M -m aoc.year2015.day01

# Or from repository root
cd clojure && clojure -M -m aoc.year2015.day01
```

### Code Style
- Clojure 1.12.0 with modern features
- Use `cljfmt` for consistent formatting
- Use `clj-kondo` for linting
- Comprehensive docstrings on all public functions
- Functional programming patterns and immutable data structures

### Helper Library Usage
Most solutions should leverage the helper library for common operations:
- Input reading: `(input/read-lines filepath)`, `(input/read-grid filepath)`, `(input/parse-numbers text)`
- Point operations: `(point/add p1 p2)`, `(point/manhattan-distance p1 p2)`, direction constants (NORTH, SOUTH, EAST, WEST)
- Grid operations: `(grid/make-grid rows)`, `(grid/grid-get grid point)`, `(grid/grid-neighbors-4 grid point)`
- Pathfinding: `(pathfinding/bfs start neighbors-fn goal?)`, `(pathfinding/dijkstra start neighbors-fn goal?)`, `(pathfinding/a-star start neighbors-fn heuristic-fn goal?)`
- Mathematical utilities: `(math/gcd a b)`, `(math/lcm a b)`, `(math/primes-up-to n)`, `(math/factorial n)`
- Utility functions: `(utils/count-if pred coll)`, `(utils/parse-int s)`, `(utils/print-solution part answer)`

## Input Files

Input files are typically stored in:
- Python: `python/YEAR/input/DAY.txt` or referenced with relative paths in solutions
- JavaScript: `../../../aoc-data/YEAR/DAY/input` (relative to solution directory)
- Go: `../../../aoc-data/YEAR/DAY/input` (relative to solution directory, use `input.GetInputPath(year, day)`)
- C: `../../../aoc-data/YEAR/DAY/input` (relative to solution directory)
- Clojure: `../../../aoc-data/YEAR/DAY/input` (relative to solution directory)
- Scheme: `../../../aoc-data/YEAR/DAY/input` (relative to solution directory)
- Perl: `../../../aoc-data/YEAR/DAY/input` (relative to solution directory)

## Solution Patterns

### Python Pattern
```python
from aoc_helpers import AoCInput, Grid2D, AoCUtils

def solve_part1():
    lines = AoCInput.read_lines("input.txt")
    # Solution logic
    return result

answer = solve_part1()
AoCUtils.print_solution(1, answer)
```

### JavaScript Pattern
```javascript
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const INPUT_FILE = join(__dirname, '../../../aoc-data/YEAR/DAY/input');

function solvePart1() {
  const input = readFileSync(INPUT_FILE, 'utf-8').trim();
  // Solution logic
  return answer;
}

const answer = solvePart1();
console.log(`Part 1: ${answer}`);
```

### Go Pattern
```go
package main

// Advent of Code YEAR - Day X: Title
// https://adventofcode.com/YEAR/day/X

import (
    "github.com/dneff/adventofcode/go/pkg/input"
    "github.com/dneff/adventofcode/go/pkg/utils"
)

func solvePart1(lines []string) int {
    // Solution logic here
    return answer
}

func main() {
    inputPath := input.GetInputPath(YEAR, DAY)
    lines := input.MustReadLines(inputPath)

    answer := solvePart1(lines)
    utils.PrintSolution(1, answer)
}
```

### Scheme/Racket Pattern
```racket
#lang racket

;; Advent of Code YEAR - Day X: Title
;; https://adventofcode.com/YEAR/day/X

(require "../../helpers/input.rkt")
(require "../../helpers/utils.rkt")

;; Input file path
(define INPUT-FILE "../../../aoc-data/YEAR/X/input")

;; Part 1 solution
(define (solve-part1)
  (define lines (read-lines INPUT-FILE))
  ;; Solution logic here
  (define answer 0)
  answer)

;; Compute and print answer
(print-solution 1 (solve-part1))
```

### C Pattern
```c
/*
 * Advent of Code YEAR - Day X: Title
 * https://adventofcode.com/YEAR/day/X
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
    get_input_path(YEAR, DAY, input_path, sizeof(input_path));

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

### Perl Pattern
```perl
#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;

# Advent of Code YEAR - Day X: Title
# https://adventofcode.com/YEAR/day/X

use lib '../../lib';
use AoC::Input qw(read_lines);
use AoC::Utils qw(print_solution);

sub solve_part1
{
    my @lines = read_lines('input');
    # Solution logic
    my $answer = 0;
    return $answer;
}

my $answer = solve_part1();
print_solution(1, $answer);
```

### Clojure Pattern
```clojure
(ns aoc.yearYYYY.dayDD
  "Advent of Code YEAR - Day D: Title
   https://adventofcode.com/YEAR/day/D"
  (:require [aoc.input :as input]
            [aoc.utils :as utils]))

;; Input file path
(def INPUT-FILE "../../../aoc-data/YEAR/D/input")

(defn solve-part1
  "Solution for part 1."
  []
  (let [lines (input/read-lines INPUT-FILE)]
    ;; Solution logic here
    0))

(defn solve-part2
  "Solution for part 2."
  []
  (let [lines (input/read-lines INPUT-FILE)]
    ;; Solution logic here
    0))

(defn -main []
  (utils/print-solution 1 (solve-part1))
  (utils/print-solution 2 (solve-part2)))
```

## Utility Scripts

### Verify Python Solutions
Verify Python solutions against known correct answers:
```bash
# From repository root
python python/verify_solutions.py              # Verify all years
python python/verify_solutions.py 2015         # Verify specific year
python python/verify_solutions.py 2015 20      # Verify specific day
python python/verify_solutions.py --write-missing  # Write missing answers
```

### Verify JavaScript Solutions
Verify JavaScript solutions against known correct answers:
```bash
# From repository root
cd javascript
npm run verify                    # Verify all years
npm run verify -- 2015            # Verify specific year
npm run verify -- 2015 20         # Verify specific day
npm run verify -- --write-missing # Write missing answers

# Or directly with node
node javascript/verify_solutions.js 2015
```

### Verify Go Solutions
Verify Go solutions against known correct answers:
```bash
# From go/ directory
cd go
go run verify_solutions.go                # Verify all years
go run verify_solutions.go 2015           # Verify specific year
go run verify_solutions.go 2015 1         # Verify specific day
go run verify_solutions.go --year 2015 --day 1 --write-missing
```

### Verify Scheme Solutions
Verify Scheme solutions against known correct answers:
```bash
# From repository root
racket scheme/verify_solutions.rkt              # Verify all years
racket scheme/verify_solutions.rkt 2015         # Verify specific year
racket scheme/verify_solutions.rkt 2015 20      # Verify specific day
racket scheme/verify_solutions.rkt --year 2015 --day 20 --write-missing
```

### Verify C Solutions
Verify C solutions against known correct answers:
```bash
# From c/ directory
make verify                        # Build verification program
./verify_solutions                 # Verify all years
./verify_solutions 2015            # Verify specific year
./verify_solutions 2015 1          # Verify specific day
./verify_solutions --year 2015 --day 1 --write-missing
```

### Verify Perl Solutions
Verify Perl solutions against known correct answers:
```bash
# From repository root
perl perl/verify_solutions.pl                   # Verify all years
perl perl/verify_solutions.pl 2015              # Verify specific year
perl perl/verify_solutions.pl 2015 20           # Verify specific day
perl perl/verify_solutions.pl --year 2015 --day 20 --write-missing
```

### Verify Clojure Solutions
Verify Clojure solutions against known correct answers:
```bash
# From clojure/ directory
clojure -M verify_solutions.clj              # Verify all years
clojure -M verify_solutions.clj 2015         # Verify specific year
clojure -M verify_solutions.clj 2015 20      # Verify specific day
clojure -M verify_solutions.clj --year 2015 --day 20 --write-missing
```

### Refactor Solutions
Refactor solution files to use the helper library:
```bash
python python/refactor_solutions.py
```

## Development Notes

- Solutions are typically split into `solution1.py`/`solution2.py` for the two parts of each day's challenge
- Some solutions use specialized classes (e.g., `IntCode.py` for 2019 IntCode problems)
- The helper library consolidates patterns from 300+ solutions across all years
- Input files may be shared between solutions or stored in year-specific input directories
- **Repository organization**: Keep root directory clean - all language-specific files (including scripts) go in language subdirectories