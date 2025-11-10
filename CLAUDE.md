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
├── go/              # Go solutions (2022)
│   └── 2022/
│       ├── helpers/ # Helper functions
│       └── DAY/     # solution1.go, solution2.go
└── scheme/          # Racket/Scheme solutions (2015)
    ├── helpers/     # Helper library modules
    └── 2015/        # Year-organized solutions
        └── DAY/     # solution1.rkt, solution2.rkt
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

## Go Development

### Structure
- Module name: `advent` (defined in `go/2022/go.mod`)
- Go version: 1.19
- Helper package: `advent/helpers` with utilities for conversions, slices, and verification

### Running Solutions
```bash
# Run from go/2022/ directory
cd go/2022/DAY
go run solution1.go
go run solution2.go
```

### Helper Functions
- `advent.Max()`: Find maximum in slice
- `advent.GetInt()`: String to int conversion with error handling
- `advent.Check()`: Error checking utility

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

## Input Files

Input files are typically stored in:
- Python: `python/YEAR/input/DAY.txt` or referenced with relative paths in solutions
- Go: `input/DAY.txt` (relative to solution directory)
- Scheme: `../../../aoc-data/YEAR/DAY/input` (relative to solution directory)

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

### Go Pattern
```go
package main

import (
    advent "advent/helpers"
    // other imports
)

func main() {
    // Read input
    // Solution logic
    fmt.Printf("The solution is: %v \n", result)
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

### Verify Scheme Solutions
Verify Scheme solutions against known correct answers:
```bash
# From repository root
racket scheme/verify_solutions.rkt              # Verify all years
racket scheme/verify_solutions.rkt 2015         # Verify specific year
racket scheme/verify_solutions.rkt 2015 20      # Verify specific day
racket scheme/verify_solutions.rkt --year 2015 --day 20 --write-missing
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