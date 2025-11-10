# Advent of Code - Racket/Scheme Solutions

This directory contains Racket (Scheme dialect) solutions for Advent of Code challenges, demonstrating functional programming approaches to algorithmic problems.

## Prerequisites

Install Racket from [racket-lang.org](https://racket-lang.org/) or via package manager:

```bash
# macOS
brew install racket

# Ubuntu/Debian
sudo apt-get install racket

# Arch Linux
sudo pacman -S racket
```

## Directory Structure

```
scheme/
├── helpers/          # Helper library modules
│   ├── input.rkt     # File I/O and parsing
│   ├── point.rkt     # Coordinate handling
│   ├── grid.rkt      # 2D grid operations
│   ├── math.rkt      # Mathematical utilities
│   ├── utils.rkt     # Functional utilities
│   └── pathfinding.rkt # BFS, Dijkstra, A*
└── 2015/            # Year-organized solutions
    ├── 01/          # Day 1
    │   ├── solution1.rkt
    │   └── solution2.rkt
    └── ...
```

## Running Solutions

From the repository root:

```bash
racket scheme/2015/01/solution1.rkt
racket scheme/2015/01/solution2.rkt
```

Or directly from the solution directory:

```bash
cd scheme/2015/01
racket solution1.rkt
```

## Helper Library Documentation

### input.rkt - File I/O and Parsing

```racket
(require "../../helpers/input.rkt")

;; Read all lines from a file
(read-lines "input.txt")
; => '("line1" "line2" ...)

;; Preserve leading spaces
(read-lines "input.txt" #:preserve-leading-space? #t)

;; Read entire file as string
(read-file "input.txt")
; => "file contents..."

;; Read as 2D grid (hash table)
(read-grid "input.txt")
; => #hash(((0 . 0) . #\a) ((1 . 0) . #\b) ...)

;; Read lines as integers
(read-numbers "input.txt")
; => '(123 456 789)

;; Read sections separated by empty lines
(read-sections "input.txt")
; => '(("section1-line1" "section1-line2") ("section2-line1"))

;; Extract all integers from a string
(parse-numbers "abc 123 def -456")
; => '(123 -456)
```

### point.rkt - Coordinate Handling

```racket
(require "../../helpers/point.rkt")

;; Create a point
(define p1 (point 3 4))

;; Accessors
(point-x p1)  ; => 3
(point-y p1)  ; => 4

;; Arithmetic
(point-add p1 (point 1 2))      ; => (4 . 6)
(point-sub p1 (point 1 1))      ; => (2 . 3)
(point-multiply p1 2)           ; => (6 . 8)
(point-manhattan-distance p1 (point 0 0))  ; => 7

;; Direction constants
NORTH   ; => (0 . -1)
SOUTH   ; => (0 . 1)
EAST    ; => (1 . 0)
WEST    ; => (-1 . 0)

;; Get neighbors
(point-neighbors-4 (point 0 0))
; => '((0 . -1) (0 . 1) (1 . 0) (-1 . 0))

(point-neighbors-8 (point 0 0))
; => includes diagonals

;; Direction utilities
(char->direction #\^)  ; => (0 . -1)
(turn-left NORTH)      ; => WEST
(turn-right NORTH)     ; => EAST
```

### grid.rkt - 2D Grid Operations

```racket
(require "../../helpers/grid.rkt")

;; Create grid from list of strings
(define g (make-grid '("abc" "def")))

;; Grid access
(grid-ref g (point 0 0))          ; => #\a
(grid-ref g (point 5 5) #\.)      ; => #\. (default)
(grid-contains? g (point 1 1))    ; => #t

;; Grid modification (functional - returns new grid)
(define g2 (grid-set! g (point 0 0) #\X))

;; Grid dimensions
(grid-width g)   ; => 3
(grid-height g)  ; => 2
(grid-bounds g)  ; => '(0 0 2 1)  ; (min-x min-y max-x max-y)

;; Grid queries
(grid-positions g)  ; => all coordinate pairs
(grid-values g)     ; => all characters

;; Find positions matching predicate
(grid-find g (lambda (c) (equal? c #\a)))  ; => '((0 . 0))
(grid-count g (lambda (c) (equal? c #\a))) ; => 1

;; Neighbors
(grid-neighbors-4 g (point 1 1))  ; => valid 4-directional neighbors
(grid-neighbors-8 g (point 1 1))  ; => valid 8-directional neighbors

;; Display for debugging
(grid-display g)
```

### math.rkt - Mathematical Utilities

```racket
(require "../../helpers/math.rkt")

;; Basic operations
(gcd 12 8)           ; => 4
(lcm 4 6)            ; => 12
(lcm-list '(4 6 8))  ; => 24

;; Combinatorics
(factorial 5)         ; => 120
(combinations 5 2)    ; => 10  (5 choose 2)
(permutations 5 2)    ; => 20  (5 P 2)

;; Number theory
(divisors 12)         ; => '(1 2 3 4 6 12)
(prime? 17)           ; => #t
(primes-up-to 20)     ; => '(2 3 5 7 11 13 17 19)

;; Modular arithmetic
(mod-pow 2 10 1000)   ; => 24  (2^10 mod 1000)

;; Digit operations
(digits 12345)         ; => '(1 2 3 4 5)
(digits->number '(1 2 3))  ; => 123

;; List operations
(sum '(1 2 3 4))      ; => 10
(product '(2 3 4))    ; => 24
```

### utils.rkt - Functional Utilities

```racket
(require "../../helpers/utils.rkt")

;; Output formatting
(print-solution 1 answer)  ; => "Part 1: answer"

;; List utilities
(count-if odd? '(1 2 3 4 5))     ; => 3
(find-first even? '(1 3 4 5))    ; => 4
(frequencies '(a b a c b a))     ; => #hash((a . 3) (b . 2) (c . 1))

;; Partitioning
(partition-by even? '(2 4 1 3 6 8))
; => '((2 4) (1 3) (6 8))

(group-by (lambda (x) (modulo x 2)) '(1 2 3 4))
; => #hash((0 . (4 2)) (1 . (3 1)))

;; Sequences
(range 5)           ; => '(0 1 2 3 4)
(range 2 5)         ; => '(2 3 4)
(repeat 3 'x)       ; => '(x x x)

;; Conditional sequences
(take-while (lambda (x) (< x 5)) '(1 2 3 6 7))  ; => '(1 2 3)
(drop-while (lambda (x) (< x 5)) '(1 2 3 6 7))  ; => '(6 7)

;; Function utilities
(define cached-fib (memoize fibonacci))
(apply-n (lambda (x) (* x 2)) 3 5)  ; => 40  (5 * 2^3)
```

### pathfinding.rkt - Graph Algorithms

```racket
(require "../../helpers/pathfinding.rkt")

;; BFS - find path to specific goal
(define neighbors
  (lambda (pos) (list (+ pos 1) (- pos 1))))
(bfs neighbors 0 (lambda (n) (= n 10)))
; => '(0 1 2 3 4 5 6 7 8 9 10)  ; path

;; BFS - find all reachable nodes
(bfs-all-paths neighbors 0)
; => set of all reachable positions

;; Dijkstra - weighted graph shortest path
(define weighted-neighbors
  (lambda (pos)
    (list (cons (+ pos 1) 1)    ; (neighbor . cost)
          (cons (+ pos 2) 3))))
(dijkstra weighted-neighbors 0 10)
; => '((path...) . total-cost)

;; A* - with heuristic
(define heuristic
  (lambda (pos goal)
    (abs (- goal pos))))
(a-star weighted-neighbors heuristic 0 10)
; => '((path...) . total-cost)
```

## Solution Template

Standard template for Racket solutions:

```racket
#lang racket

;; Advent of Code 2015 - Day X: Title
;; https://adventofcode.com/2015/day/X

(require "../../helpers/input.rkt")
(require "../../helpers/utils.rkt")

;; Input file path
(define INPUT-FILE "../../../aoc-data/2015/X/input")

;; Part 1 solution
(define (solve-part1)
  (define lines (read-lines INPUT-FILE))
  ;; Solution logic here
  (define answer 0)
  answer)

;; Compute and print answer
(print-solution 1 (solve-part1))
```

## Input Files

Solutions expect input files at `../../../aoc-data/YEAR/DAY/input` relative to the solution file. This follows the aoc-data repository structure used by Python solutions.

## Code Style

- Use functional programming patterns
- Prefer immutable data structures
- Use meaningful function and variable names
- Add comments for complex logic
- Keep functions focused and composable

## Development Workflow

1. Read problem statement
2. Create solution file from template
3. Import required helper modules
4. Implement solution using helper library
5. Test with example input
6. Run with actual input
7. Submit answer

## Performance

Racket's JIT compiler provides good performance for most AoC problems. For computationally intensive problems, consider:

- Using typed/racket for better optimization
- Memoization for recursive functions
- Efficient data structures (vectors for arrays, sets for membership)
- Lazy evaluation with streams for infinite sequences

## Resources

- [Racket Documentation](https://docs.racket-lang.org/)
- [Racket Guide](https://docs.racket-lang.org/guide/)
- [Advent of Code](https://adventofcode.com/)
