# Go Advent of Code Solutions

This directory contains Go implementations of Advent of Code solutions with a comprehensive helper library.

## Structure

```
go/
├── pkg/              # Helper library packages
│   ├── input/        # File reading and parsing utilities
│   ├── point/        # 2D point operations and direction constants
│   ├── grid/         # Generic Grid[T] type with operations
│   ├── math/         # Mathematical utilities (GCD, LCM, primes, etc.)
│   ├── pathfinding/  # BFS and Dijkstra implementations
│   └── utils/        # Common patterns and formatting utilities
├── 2015/             # 2015 solutions (days 1-25)
├── 2022/             # 2022 solutions (days 1-4)
├── verify_solutions.go  # Verification tool
├── go.mod            # Module definition (Go 1.22+)
└── README.md         # This file
```

## Requirements

- Go 1.22 or later

## Running Solutions

```bash
# Navigate to the year directory
cd 2015/01

# Run part 1
go run solution1.go

# Run part 2
go run solution2.go
```

## Helper Library Usage

### Input Package

The `input` package provides utilities for reading and parsing input files:

```go
import "github.com/dneff/adventofcode/go/pkg/input"

// Read entire file as string
content := input.MustReadFile("input.txt")

// Read file as lines
lines := input.MustReadLines("input.txt")

// Read file as 2D rune grid
grid := input.MustReadGrid("input.txt")

// Parse integers from a string
nums := input.ParseInts("1, 2, -3, 4")  // []int{1, 2, -3, 4}

// Get path to aoc-data input file
inputPath := input.GetInputPath(2015, 1)  // "../../../aoc-data/2015/1/input"
```

### Point Package

The `point` package provides 2D coordinate operations:

```go
import "github.com/dneff/adventofcode/go/pkg/point"

// Create a point
p := point.New(3, 4)

// Vector operations
p2 := p.Add(point.North)     // Move north
p3 := p.Manhattan(p2)        // Manhattan distance

// Direction constants
point.North   // {0, -1}
point.South   // {0, 1}
point.East    // {1, 0}
point.West    // {-1, 0}

// Get neighbors
neighbors := p.Neighbors4()  // 4 orthogonal neighbors
neighbors8 := p.Neighbors8() // 8 neighbors (including diagonals)

// Rotations
p4 := p.RotateLeft()        // 90° counterclockwise
p5 := p.RotateRight()       // 90° clockwise

// Parse direction from character
dir := point.ParseDirection('^')  // Returns point.North
```

### Grid Package

The `grid` package provides a generic 2D grid type:

```go
import "github.com/dneff/adventofcode/go/pkg/grid"

// Create grid from lines
g := grid.FromLines(input.MustReadLines("input.txt"))

// Access cells
value := g.Get(point.New(x, y))
g.Set(point.New(x, y), '#')

// Check bounds
if g.Contains(p) {
    // Point is within grid
}

// Find cells
pos, found := g.Find('S', func(a, b rune) bool { return a == b })
allMatches := g.FindAll(func(r rune) bool { return r == '#' })

// Get neighbors
neighbors := g.Neighbors4(p)  // Only valid neighbors

// Iterate over all cells
g.ForEach(func(p point.Point, value rune) {
    // Process each cell
})

// Count matching cells
count := g.Count(func(r rune) bool { return r == '#' })
```

### Math Package

The `math` package provides mathematical utilities:

```go
import "github.com/dneff/adventofcode/go/pkg/math"

// Basic operations
a := math.Abs(-5)           // 5
m := math.Min(3, 7)         // 3
M := math.Max(3, 7)         // 7

// GCD and LCM
gcd := math.GCD(12, 18)     // 6
lcm := math.LCM(12, 18)     // 36
lcmAll := math.LCMSlice([]int{12, 18, 24})  // 72

// Primes
isPrime := math.IsPrime(17) // true
primes := math.PrimesUpTo(20)  // [2, 3, 5, 7, 11, 13, 17, 19]

// Combinatorics
fact := math.Factorial(5)        // 120
comb := math.Combinations(5, 2)  // 10 (C(5,2))
perm := math.Permutations(5, 2)  // 20 (P(5,2))

// Power
p := math.Pow(2, 10)             // 1024
pm := math.PowMod(2, 100, 97)    // (2^100) % 97

// Slice operations
sum := math.Sum([]int{1, 2, 3, 4})      // 10
prod := math.Product([]int{2, 3, 4})    // 24
max := math.MaxSlice([]int{1, 5, 3})    // 5
```

### Pathfinding Package

The `pathfinding` package provides graph search algorithms:

```go
import "github.com/dneff/adventofcode/go/pkg/pathfinding"

// BFS to find shortest path distance
distance := pathfinding.BFS(
    start,
    func(s State) bool { return s == goal },
    func(s State) []State { return getNeighbors(s) },
)

// BFS to get the actual path
path := pathfinding.BFSPath(start, goalFunc, neighborsFunc)

// BFS to explore all reachable states
distances := pathfinding.BFSAll(start, neighborsFunc)

// Dijkstra for weighted graphs
cost := pathfinding.Dijkstra(
    start,
    goalFunc,
    func(s State) []pathfinding.Edge[State] {
        // Return weighted edges
        return []pathfinding.Edge[State]{
            {State: neighbor1, Cost: 5},
            {State: neighbor2, Cost: 3},
        }
    },
)

// Dijkstra to get path
path := pathfinding.DijkstraPath(start, goalFunc, weightedNeighborsFunc)

// Dijkstra to all reachable states
allCosts := pathfinding.DijkstraAll(start, weightedNeighborsFunc)
```

### Utils Package

The `utils` package provides common utility functions:

```go
import "github.com/dneff/adventofcode/go/pkg/utils"

// Print solution in standard format
utils.PrintSolution(1, answer)  // "Part 1: 42"

// Error handling
utils.Check(err)                // Panics if err != nil
val := utils.Must1(fn())        // Returns value, panics on error

// Functional operations
filtered := utils.Filter(nums, func(n int) bool { return n > 0 })
squared := utils.Map(nums, func(n int) int { return n * n })
sum := utils.Reduce(nums, 0, func(acc, n int) int { return acc + n })

// Predicates
allPositive := utils.All(nums, func(n int) bool { return n > 0 })
anyNegative := utils.Any(nums, func(n int) bool { return n < 0 })
hasValue := utils.Contains(slice, value)

// Slice operations
reversed := utils.Reverse(slice)
unique := utils.Unique(slice)
chunks := utils.Chunk(slice, 3)

// Collections
freq := utils.Frequencies([]int{1, 2, 2, 3, 3, 3})  // map[1:1 2:2 3:3]
groups := utils.GroupBy(items, keyFunc)

// Sets
set := utils.SetFromSlice([]int{1, 2, 3, 2, 1})
union := utils.SetUnion(setA, setB)
intersection := utils.SetIntersection(setA, setB)

// Memoization
fib := utils.Memoize(func(n int) int {
    if n <= 1 {
        return n
    }
    return fib(n-1) + fib(n-2)
})
```

## Verification

The `verify_solutions.go` tool runs solutions and compares outputs against known correct answers:

```bash
# From go/ directory
go run verify_solutions.go              # Verify all years
go run verify_solutions.go 2015         # Verify year 2015
go run verify_solutions.go 2015 1       # Verify day 1 of 2015
go run verify_solutions.go --year 2015 --day 1 --write-missing
```

## Solution Template

```go
package main

import (
    "github.com/dneff/adventofcode/go/pkg/input"
    "github.com/dneff/adventofcode/go/pkg/utils"
)

func solvePart1(lines []string) int {
    // Solution logic here
    return answer
}

func main() {
    inputPath := input.GetInputPath(2015, 1)
    lines := input.MustReadLines(inputPath)

    answer := solvePart1(lines)
    utils.PrintSolution(1, answer)
}
```

## Code Style

- Follow standard Go conventions (`gofmt`, `go vet`)
- Use the helper library for common operations
- Keep functions focused and composable
- Leverage Go generics (Go 1.22+) for type-safe abstractions
- Use meaningful variable and function names

## Notes

- Input files are stored in `../aoc-data/YEAR/DAY/input` relative to solution files
- Solutions use Go modules for dependency management
- The helper library provides both panicking (`Must*`) and error-returning variants
- Generic types allow the same algorithms to work with different data types
