# Advent of Code Python Solutions

This directory contains Python solutions for Advent of Code challenges from 2015-2024, along with a comprehensive helper library to streamline common operations.

## Using the Helper Library

The `aoc_helpers.py` module provides utilities commonly used across AoC solutions. Import it in your solutions:

```python
from aoc_helpers import AoCInput, Grid2D, Point2D, Pathfinding, MathUtils, Directions, AoCUtils
```

## Quick Reference

### Input Reading

```python
# Read all lines from file
lines = AoCInput.read_lines("input.txt")

# Read into a 2D grid dictionary
grid = AoCInput.read_grid("input.txt")

# Read all numbers from file
numbers = AoCInput.read_numbers("input.txt")

# Split file by empty lines into sections
sections = AoCInput.read_sections("input.txt")

# Extract numbers from any string
nums = AoCInput.parse_numbers("move 5 from 3 to 7")  # [5, 3, 7]
```

### Grid Operations

```python
# Create grid from lines or existing dictionary
grid = Grid2D(lines)
grid = Grid2D(existing_dict)

# Access grid positions
value = grid[(x, y)]
grid[(x, y)] = 'X'

# Check if position exists
if (x, y) in grid:
    print("Position exists")

# Get adjacent positions (4 or 8 directions)
neighbors = grid.get_adjacent((x, y))
neighbors = grid.get_adjacent((x, y), include_diagonals=True)

# Find all positions with specific value
start_positions = grid.find_positions('S')

# Get grid dimensions
width, height = grid.get_dimensions()

# Print grid for debugging
grid.print_grid()
```

### Point Operations

```python
# Create and manipulate points
p1 = Point2D(3, 4)
p2 = Point2D(1, 2)

# Arithmetic operations
p3 = p1 + p2  # Point2D(4, 6)
p4 = p1 - p2  # Point2D(2, 2)

# Distance calculation
distance = p1.manhattan_distance(p2)  # 4

# Get adjacent positions
adjacent = p1.adjacent_positions()  # 4 cardinal directions
adjacent = p1.adjacent_positions(include_diagonals=True)  # 8 directions

# Convert to tuple
pos = p1.to_tuple()  # (3, 4)
```

### Direction Handling

```python
# Use predefined direction constants
for direction in Directions.CARDINAL:
    new_pos = (x + direction[0], y + direction[1])

# Convert direction names to vectors
direction = Directions.DIRECTION_MAP["N"]  # (0, -1)
direction = Directions.ARROW_MAP["^"]      # (0, -1)

# Turn directions
new_dir = Directions.turn_right((0, -1))  # (1, 0)
new_dir = Directions.turn_left((0, -1))   # (-1, 0)
```

### Pathfinding

```python
# BFS to find shortest path
def get_neighbors(pos):
    x, y = pos
    return [(x+dx, y+dy) for dx, dy in Directions.CARDINAL 
            if (x+dx, y+dy) in grid]

path = Pathfinding.bfs(start, goal, get_neighbors)
distance = Pathfinding.bfs_distance(start, goal, get_neighbors)

# Dijkstra for weighted graphs
def get_weighted_neighbors(pos):
    # Return list of (neighbor, cost) tuples
    return [(neighbor, cost) for neighbor, cost in neighbors_with_costs]

min_cost = Pathfinding.dijkstra(start, goal, get_weighted_neighbors)
```

### Mathematical Utilities

```python
# GCD and LCM
result = MathUtils.gcd_multiple(12, 18, 24)  # 6
result = MathUtils.lcm_multiple(4, 6, 8)     # 24

# Manhattan distance
dist = MathUtils.manhattan_distance((0, 0), (3, 4))  # 7

# Sign function
sign = MathUtils.sign(-5)  # -1
```

### Coordinate Counting

```python
# Count overlapping coordinates
counter = Counter2D()
counter.add((1, 1))
counter.add((1, 1))  # Now has count of 2

# Find positions with specific counts
overlapping = counter.positions_above_threshold(2)
```

### Utility Functions

```python
# Standard solution printing
AoCUtils.print_solution(1, answer)  # "Part 1: answer"

# Split list into chunks
chunks = AoCUtils.chunks([1,2,3,4,5,6], 3)  # [[1,2,3], [4,5,6]]

# Convert binary to decimal
decimal = AoCUtils.binary_to_decimal("1010")  # 10

# Character priority (for problems like 2022 day 3)
priority = AoCUtils.char_to_priority('a')  # 1
priority = AoCUtils.char_to_priority('A')  # 27
```

## Example Usage

Here's how a typical solution might look using the helpers:

```python
from aoc_helpers import AoCInput, Grid2D, Pathfinding, AoCUtils

def solve_part1():
    # Read input
    lines = AoCInput.read_lines("input.txt")
    grid = Grid2D(lines)
    
    # Find start and end positions
    start = grid.find_positions('S')[0]
    goal = grid.find_positions('E')[0]
    
    # Define neighbor function
    def get_neighbors(pos):
        return [n for n in grid.get_adjacent(pos) if grid[n] != '#']
    
    # Find shortest path
    distance = Pathfinding.bfs_distance(start, goal, get_neighbors)
    
    return distance

# Run solution
answer = solve_part1()
AoCUtils.print_solution(1, answer)
```

## Directory Structure

```
python/
├── aoc_helpers.py          # Helper library
├── README.md              # This file
├── 2015/                  # Solutions by year
│   ├── 01/
│   │   ├── solution1.py
│   │   └── solution2.py
│   └── ...
├── 2016/
└── ...
```

## Tips

1. **Import selectively**: Only import the classes you need to keep your solutions clean
2. **Custom neighbor functions**: The pathfinding algorithms accept custom neighbor functions, making them flexible for different grid types and movement rules
3. **Grid flexibility**: Grid2D accepts both dictionaries and list of strings, so you can use whichever input format is more convenient
4. **Debugging**: Use `grid.print_grid()` to visualize your grid state during development

The helper library eliminates most boilerplate code while remaining flexible enough to handle the diverse range of AoC problems.