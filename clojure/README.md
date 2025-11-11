# Advent of Code - Clojure Solutions

This directory contains Clojure solutions for Advent of Code challenges, organized with a comprehensive helper library and modern Clojure tooling.

## Project Structure

```
clojure/
├── src/aoc/              # Source code
│   ├── input.clj         # File I/O and parsing utilities
│   ├── point.clj         # 2D point operations
│   ├── grid.clj          # 2D grid operations
│   ├── math.clj          # Mathematical utilities
│   ├── pathfinding.clj   # Search algorithms (BFS, Dijkstra, A*)
│   ├── utils.clj         # General utilities
│   └── year2015/         # 2015 solutions by day
├── test/aoc/             # Test files
├── resources/            # Resource files
├── deps.edn              # Dependency configuration
├── verify_solutions.clj  # Solution verification script
└── README.md             # This file
```

## Installation

### Prerequisites

- [Clojure CLI](https://clojure.org/guides/getting_started) (version 1.11.0 or higher)
- Java 11 or higher

### Setup

Clone the repository and navigate to the Clojure directory:

```bash
cd adventofcode/clojure
```

Dependencies will be automatically downloaded when you first run any Clojure command.

## Running Solutions

### From the Command Line

Run a specific day's solution:

```bash
# From the clojure/ directory
clojure -M -m aoc.year2015.day01
clojure -M -m aoc.year2015.day02
```

### Using the REPL

Start a REPL:

```bash
clojure -M:repl
```

Then load and run a solution:

```clojure
(require '[aoc.year2015.day01 :as day01])
(day01/solve-part1)
; => 232

(day01/solve-part2)
; => 1783
```

### Verifying Solutions

The verification script runs solutions and compares outputs against known correct answers from the `aoc-data` repository:

```bash
# Verify all years
clojure -M verify_solutions.clj

# Verify specific year
clojure -M verify_solutions.clj 2015

# Verify specific day
clojure -M verify_solutions.clj 2015 1

# Write missing answers
clojure -M verify_solutions.clj 2015 1 --write-missing
```

## Helper Library

The helper library provides utilities for common Advent of Code operations. All helper namespaces are fully documented with docstrings.

### Input Module (`aoc.input`)

File reading and parsing utilities:

```clojure
(require '[aoc.input :as input])

;; Read lines from a file
(input/read-lines "input.txt")
; => ["line1" "line2" "line3"]

;; Read entire file as text
(input/read-text "input.txt")
; => "line1\nline2\nline3"

;; Parse all numbers from text
(input/parse-numbers "x=10, y=-5, z=20")
; => (10 -5 20)

;; Read file as 2D grid
(input/read-grid "grid.txt")
; => [[\# \. \.] [\. \# \.]]

;; Read blocks separated by blank lines
(input/read-blocks "input.txt")
; => [["line1" "line2"] ["line3" "line4"]]
```

### Point Module (`aoc.point`)

2D point operations and direction handling:

```clojure
(require '[aoc.point :as point])

;; Direction constants
point/NORTH   ; => [0 -1]
point/SOUTH   ; => [0 1]
point/EAST    ; => [1 0]
point/WEST    ; => [-1 0]

;; Point operations
(point/add [1 2] [3 4])
; => [4 6]

(point/manhattan-distance [0 0] [3 4])
; => 7

(point/move [5 5] point/NORTH 3)
; => [5 2]

;; Get neighbors
(point/neighbors-4 [5 5])
; => [[5 4] [6 5] [5 6] [4 5]]

(point/neighbors-8 [5 5])
; => [[5 4] [6 4] [6 5] [6 6] [5 6] [4 6] [4 5] [4 4]]

;; Direction rotation
(point/rotate-right point/NORTH)
; => [1 0]  (EAST)

(point/rotate-left point/NORTH)
; => [-1 0]  (WEST)
```

### Grid Module (`aoc.grid`)

2D grid operations:

```clojure
(require '[aoc.grid :as grid])

;; Create a grid
(def my-grid (grid/make-grid ["#.." ".#." "..#"]))

;; Grid dimensions
(grid/grid-width my-grid)   ; => 3
(grid/grid-height my-grid)  ; => 3

;; Get and set values
(grid/grid-get my-grid [0 0])           ; => \#
(grid/grid-set my-grid [0 0] \.)        ; => updated grid

;; Find positions
(grid/find-positions my-grid #(= % \#))
; => [[0 0] [1 1] [2 2]]

(grid/find-position my-grid #(= % \#))
; => [0 0]  (first match)

;; Get neighbors
(grid/grid-neighbors-4 my-grid [1 1])
; => [[1 0] [2 1] [1 2] [0 1]]

;; Count matching positions
(grid/grid-count #(= % \#) my-grid)
; => 3
```

### Math Module (`aoc.math`)

Mathematical utilities:

```clojure
(require '[aoc.math :as math])

;; GCD and LCM
(math/gcd 12 8)      ; => 4
(math/lcm 12 8)      ; => 24
(math/lcm-of [3 4 5])  ; => 60

;; Primes
(math/is-prime? 17)  ; => true
(math/primes-up-to 20)
; => (2 3 5 7 11 13 17 19)

(math/prime-factors 60)
; => [2 2 3 5]

;; Factorials and combinatorics
(math/factorial 5)   ; => 120
(math/permutations [1 2 3])
; => [[1 2 3] [1 3 2] [2 1 3] [2 3 1] [3 1 2] [3 2 1]]

(math/combinations [1 2 3 4] 2)
; => [[1 2] [1 3] [1 4] [2 3] [2 4] [3 4]]

;; Number utilities
(math/digits 12345)      ; => [1 2 3 4 5]
(math/from-digits [1 2 3])  ; => 123

;; Statistics
(math/sum [1 2 3 4 5])      ; => 15
(math/product [2 3 4])      ; => 24
(math/mean [1 2 3 4 5])     ; => 3
(math/median [1 2 3 4 5])   ; => 3
```

### Pathfinding Module (`aoc.pathfinding`)

Search algorithms:

```clojure
(require '[aoc.pathfinding :as pathfinding])

;; Breadth-first search
(pathfinding/bfs
  [0 0]                           ; start
  (fn [pos] [[1 0] [0 1]])       ; neighbors function
  (fn [pos] (= pos [5 5])))      ; goal predicate
; => {:path [[0 0] [1 0] ... [5 5]], :visited #{...}, :distances {...}}

;; Dijkstra's algorithm
(pathfinding/dijkstra
  [0 0]
  (fn [pos] [[[1 0] 1] [[0 1] 1]])  ; neighbors with costs
  (fn [pos] (= pos [5 5])))
; => {:path [...], :distance 10, :goal [5 5]}

;; A* search
(pathfinding/a-star
  [0 0]
  (fn [pos] [[[1 0] 1] [[0 1] 1]])  ; neighbors with costs
  (fn [pos] (+ (first pos) (second pos)))  ; heuristic
  (fn [pos] (= pos [5 5])))         ; goal predicate
; => {:path [...], :distance 10, :goal [5 5]}

;; Flood fill
(pathfinding/flood-fill
  [0 0]
  (fn [pos] [[1 0] [0 1]]))  ; neighbors function
; => #{[0 0] [1 0] [0 1] ...}  ; all reachable positions
```

### Utils Module (`aoc.utils`)

General utility functions:

```clojure
(require '[aoc.utils :as utils])

;; Solution printing
(utils/print-solution 1 42)
; => "Part 1: 42"

;; Parsing
(utils/parse-int "42")       ; => 42
(utils/str->int "42")        ; => 42 (throws on error)

;; Counting and filtering
(utils/count-if even? [1 2 3 4 5])
; => 2

(utils/find-first even? [1 3 5 4 7])
; => 4

(utils/find-index even? [1 3 5 4 7])
; => 3

;; Collection utilities
(utils/transpose [[1 2 3] [4 5 6]])
; => [[1 4] [2 5] [3 6]]

(utils/min-by count [[1 2 3] [4 5] [6]])
; => [6]

(utils/max-by count [[1 2 3] [4 5] [6]])
; => [1 2 3]

;; Iteration
(utils/iterate-until inc #(> % 10) 0)
; => 11

(utils/take-until #(> % 5) (range))
; => (0 1 2 3 4 5)
```

## Code Style

### Formatting

Format code using cljfmt:

```bash
clojure -M:fmt check src/
clojure -M:fmt fix src/
```

### Linting

Lint code using clj-kondo:

```bash
clojure -M:lint --lint src/
```

### Testing

Run tests using kaocha:

```bash
clojure -M:test
# or
clojure -M:kaocha
```

## Solution Template

Here's a template for creating new solutions:

```clojure
(ns aoc.yearYYYY.dayDD
  "Advent of Code YYYY - Day D: Title
   https://adventofcode.com/YYYY/day/D"
  (:require [aoc.input :as input]
            [aoc.utils :as utils]))

;; Input file path
(def INPUT-FILE "../../../aoc-data/YYYY/D/input")

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

## Performance Tips

1. **Use transducers** for efficient data transformations:
   ```clojure
   (transduce (comp (filter even?) (map #(* % 2))) + (range 1000))
   ```

2. **Leverage lazy sequences** for large datasets:
   ```clojure
   (take 10 (filter prime? (range)))
   ```

3. **Memoize expensive functions**:
   ```clojure
   (def fib (memoize (fn [n] (if (< n 2) n (+ (fib (- n 1)) (fib (- n 2)))))))
   ```

4. **Use primitive types** for numeric operations when needed:
   ```clojure
   (defn fast-sum ^long [^long a ^long b] (+ a b))
   ```

## Dependencies

The project uses the following main dependencies:

- `org.clojure/clojure` - Clojure language (1.12.0)
- `org.clojure/data.priority-map` - Priority maps for pathfinding (1.2.0)
- `org.clojure/core.match` - Pattern matching (1.1.0)
- `org.clojure/math.combinatorics` - Combinatorics functions (0.3.0)

Development dependencies:

- `lambdaisland/kaocha` - Test runner
- `clj-kondo` - Linter
- `cljfmt` - Code formatter

## Contributing

When adding new solutions:

1. Follow the established naming convention (`dayXX.clj`)
2. Use the helper library for common operations
3. Add docstrings to all public functions
4. Run the verification script to ensure correctness
5. Format and lint your code before committing

## Resources

- [Advent of Code](https://adventofcode.com/)
- [Clojure Documentation](https://clojure.org/)
- [Clojure Style Guide](https://github.com/bbatsov/clojure-style-guide)
- [aoc-data Repository](https://github.com/dneff/aoc-data) - Contains input files and expected answers

## License

This project is part of the larger Advent of Code solutions repository. See the main repository for license information.
