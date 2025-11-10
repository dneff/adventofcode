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
└── go/              # Go solutions (2022)
    └── 2022/
        ├── helpers/ # Helper functions
        └── DAY/     # solution1.go, solution2.go
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

## Input Files

Input files are typically stored in:
- Python: `python/YEAR/input/DAY.txt` or referenced with relative paths in solutions
- Go: `input/DAY.txt` (relative to solution directory)

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

## Utility Scripts

### Verify Solutions
Verify solutions against known correct answers:
```bash
# From repository root
python python/verify_solutions.py              # Verify all years
python python/verify_solutions.py 2015         # Verify specific year
python python/verify_solutions.py 2015 20      # Verify specific day
python python/verify_solutions.py --write-missing  # Write missing answers
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