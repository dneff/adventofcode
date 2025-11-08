# JavaScript Helper Library Documentation

Comprehensive helper classes for Advent of Code solutions in JavaScript.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Classes](#classes)
  - [AoCInput](#aocinput)
  - [Point2D](#point2d)
  - [Grid2D](#grid2d)
  - [Directions](#directions)
  - [Pathfinding](#pathfinding)
  - [Counter2D](#counter2d)
  - [MathUtils](#mathutils)
  - [AoCUtils](#aocutils)
- [Usage Examples](#usage-examples)
- [Performance](#performance)

## Overview

The JavaScript helper library provides utilities for common Advent of Code tasks:
- Input file reading and parsing
- 2D coordinate and vector operations
- Grid-based data structures with efficient Map storage
- Direction constants and rotation utilities
- Graph traversal algorithms (BFS, Dijkstra)
- Coordinate counting and frequency analysis
- Mathematical functions (GCD, LCM, Manhattan distance)
- General utility functions

## Installation

```bash
cd javascript
npm install
```

## Classes

### AoCInput

Input reading and parsing utilities.

#### Methods

**`readLines(filename, preserveLeadingSpace = false)`**
- Read all lines from a file
- Returns: `string[]`
- Parameters:
  - `filename`: Path to file
  - `preserveLeadingSpace`: Keep leading whitespace if true

```javascript
import { AoCInput } from './aoc-helpers.js';

const lines = AoCInput.readLines('input.txt');
```

**`readGrid(filename)`**
- Read file into a 2D grid object
- Returns: `Object.<string, string>` with "x,y" keys
- Prefer using Grid2D class for advanced grid operations

**`readNumbers(filename)`**
- Read all integers from file (one per line)
- Returns: `number[]`

**`readSections(filename)`**
- Read file split by empty lines
- Returns: `string[][]`

**`parseNumbers(text)`**
- Extract all integers (including negative) from a string
- Returns: `number[]`

```javascript
const nums = AoCInput.parseNumbers('abc-123def456');
// Returns: [-123, 456]
```

### Point2D

2D coordinate operations with vector arithmetic.

#### Constructor

```javascript
const p = new Point2D(x, y);
```

#### Properties

- `x`: X coordinate
- `y`: Y coordinate

#### Methods

**`add(other)`**
- Add two points
- Returns: `Point2D`

**`subtract(other)`**
- Subtract two points
- Returns: `Point2D`

**`equals(other)`**
- Check equality
- Returns: `boolean`

**`manhattanDistance(other)`**
- Calculate Manhattan distance
- Returns: `number`

**`adjacentPositions(includeDiagonals = false)`**
- Get adjacent positions (4 or 8 directions)
- Returns: `Point2D[]`

**`toTuple()`**
- Convert to `[x, y]` array
- Returns: `[number, number]`

**`toString()`**
- Convert to "x,y" string
- Returns: `string`

**`Point2D.fromString(str)`** (static)
- Create Point2D from "x,y" string
- Returns: `Point2D`

#### Example

```javascript
import { Point2D } from './aoc-helpers.js';

const p1 = new Point2D(3, 4);
const p2 = new Point2D(1, 2);

const sum = p1.add(p2);           // Point2D(4, 6)
const diff = p1.subtract(p2);     // Point2D(2, 2)
const dist = p1.manhattanDistance(p2); // 5

const neighbors = p1.adjacentPositions(false); // 4 cardinal neighbors
const all8 = p1.adjacentPositions(true);       // 8 neighbors with diagonals

const str = p1.toString();        // "3,4"
const restored = Point2D.fromString(str); // Point2D(3, 4)
```

### Grid2D

2D grid operations with efficient Map-based storage.

#### Constructor

```javascript
// From string array
const grid = new Grid2D(['abc', 'def', 'ghi']);

// From Map
const map = new Map([['0,0', 'a'], ['1,0', 'b']]);
const grid = new Grid2D(map);

// From plain object
const obj = { '0,0': 'a', '1,0': 'b' };
const grid = new Grid2D(obj);
```

#### Properties

- `width`: Grid width (cached)
- `height`: Grid height (cached)
- `size`: Number of cells

#### Methods

**`get(x, y)` or `get(key)` or `get(Point2D)`**
- Get value at position
- Returns: `string | undefined`

**`set(x, y, value)` or `set(key, value)` or `set(Point2D, value)`**
- Set value at position

**`has(x, y)` or `has(key)` or `has(Point2D)`**
- Check if position exists
- Returns: `boolean`

**`delete(x, y)` or `delete(key)` or `delete(Point2D)`**
- Delete position
- Returns: `boolean`

**`getDimensions()`**
- Get grid dimensions
- Returns: `{width: number, height: number}`

**`getAdjacent(x, y, includeDiagonals)` or `getAdjacent(key, includeDiagonals)`**
- Get adjacent positions that exist in grid
- Returns: `string[]` (position keys)

**`findPositions(value)`**
- Find all positions with specific value
- Returns: `string[]`

**`inBounds(x, y)` or `inBounds(key)` or `inBounds(Point2D)`**
- Check if position is in bounds
- Returns: `boolean`

**`printGrid()`**
- Print grid to console for debugging

**Iteration methods:**
- `entries()`: Iterator of [key, value] pairs
- `keys()`: Iterator of position keys
- `values()`: Iterator of values
- `forEach(callback)`: Execute function for each entry
- Grid is iterable with `for...of`

#### Example

```javascript
import { Grid2D, Point2D } from './aoc-helpers.js';

const grid = new Grid2D(['abc', 'def', 'ghi']);

// Multiple ways to access
console.log(grid.get(0, 0));           // 'a'
console.log(grid.get('1,1'));          // 'e'
console.log(grid.get(new Point2D(2, 2))); // 'i'

// Set values
grid.set(1, 1, 'X');
grid.set('2,2', 'Y');

// Dimensions
console.log(grid.width, grid.height);  // 3, 3
console.log(grid.size);                // 9

// Find positions
const positions = grid.findPositions('a'); // ['0,0']

// Adjacent positions
const adjacent = grid.getAdjacent(1, 1, false); // 4 neighbors
const diagonal = grid.getAdjacent(1, 1, true);  // 8 neighbors

// Iteration
for (const [key, value] of grid) {
  console.log(`${key} = ${value}`);
}

// forEach
grid.forEach((value, key) => {
  console.log(`${key} = ${value}`);
});
```

### Directions

Direction constants and utilities.

#### Constants

**Cardinal directions:**
- `Directions.NORTH`: `[0, -1]`
- `Directions.EAST`: `[1, 0]`
- `Directions.SOUTH`: `[0, 1]`
- `Directions.WEST`: `[-1, 0]`

**Direction arrays:**
- `Directions.CARDINAL`: Array of 4 cardinal directions
- `Directions.ALL_8`: Array of 8 directions (including diagonals)

**Direction maps:**
- `Directions.DIRECTION_MAP`: Maps "N", "NORTH", "UP", etc. to direction vectors
- `Directions.ARROW_MAP`: Maps "^", ">", "v", "<" to direction vectors

#### Methods

**`Directions.turnRight(direction)`** (static)
- Turn 90 degrees clockwise
- Returns: `[number, number]`

**`Directions.turnLeft(direction)`** (static)
- Turn 90 degrees counter-clockwise
- Returns: `[number, number]`

#### Example

```javascript
import { Directions, Point2D, Grid2D } from './aoc-helpers.js';

// Using direction constants
const pos = new Point2D(5, 5);
const north = pos.add(new Point2D(...Directions.NORTH));

// Rotations
let dir = Directions.NORTH;
dir = Directions.turnRight(dir);  // Now EAST
dir = Directions.turnRight(dir);  // Now SOUTH

// Arrow parsing
const arrowDir = Directions.ARROW_MAP['^']; // [0, -1]

// Navigate on grid
const grid = new Grid2D(['...', '...', '...']);
let current = new Point2D(1, 1);
let facing = Directions.NORTH;

// Move forward
current = current.add(new Point2D(...facing));
// Turn right
facing = Directions.turnRight(facing);
```

### Pathfinding

Graph traversal algorithms for pathfinding and distance calculations.

#### Methods

**`Pathfinding.bfs(start, goal, getNeighbors)`** (static)
- Breadth-first search returning the complete path
- Parameters:
  - `start`: Starting position (any type)
  - `goal`: Goal position (any type)
  - `getNeighbors`: Function that takes a position and returns array of neighbor positions
- Returns: `Array | null` - Path from start to goal (inclusive), or null if no path exists

**`Pathfinding.bfsDistance(start, goal, getNeighbors)`** (static)
- BFS returning only the distance to goal
- Parameters: Same as `bfs()`
- Returns: `number` - Distance from start to goal, or -1 if no path exists

**`Pathfinding.bfsAll(start, getNeighbors)`** (static)
- BFS returning distances to all reachable positions
- Parameters:
  - `start`: Starting position (any type)
  - `getNeighbors`: Function that takes a position and returns array of neighbor positions
- Returns: `Map<string, number>` - Map of JSON-stringified positions to their distances from start

**`Pathfinding.dijkstra(start, goal, getNeighbors)`** (static)
- Dijkstra's algorithm for weighted graphs
- Parameters:
  - `start`: Starting position (any type)
  - `goal`: Goal position (any type)
  - `getNeighbors`: Function that takes a position and returns array of [neighbor, cost] tuples
- Returns: `number | null` - Shortest distance to goal, or null if no path exists

**`Pathfinding.dijkstraAll(start, getNeighbors)`** (static)
- Dijkstra's algorithm returning distances to all reachable positions
- Parameters:
  - `start`: Starting position (any type)
  - `getNeighbors`: Function that takes a position and returns array of [neighbor, cost] tuples
- Returns: `Map<string, number>` - Map of JSON-stringified positions to their distances from start

#### Example: BFS on Grid

```javascript
import { Pathfinding, Grid2D, Point2D } from './aoc-helpers.js';

const grid = new Grid2D(['S..', '.#.', '..E']);

// Define neighbor function for grid traversal
const getNeighbors = (pos) => {
  const [x, y] = pos;
  const neighbors = [];
  const directions = [[0, 1], [1, 0], [0, -1], [-1, 0]];

  for (const [dx, dy] of directions) {
    const next = [x + dx, y + dy];
    const key = `${next[0]},${next[1]}`;
    if (grid.has(key) && grid.get(key) !== '#') {
      neighbors.push(next);
    }
  }
  return neighbors;
};

// Find path from start to end
const path = Pathfinding.bfs([0, 0], [2, 2], getNeighbors);
console.log(path); // [[0,0], [1,0], [2,0], [2,1], [2,2]]

// Or just get the distance
const distance = Pathfinding.bfsDistance([0, 0], [2, 2], getNeighbors);
console.log(distance); // 4

// Get distances to all reachable positions
const distances = Pathfinding.bfsAll([0, 0], getNeighbors);
console.log(distances.get(JSON.stringify([2, 2]))); // 4
```

#### Example: Dijkstra with Weighted Graph

```javascript
import { Pathfinding } from './aoc-helpers.js';

// Graph with weighted edges
const graph = {
  'A': [['B', 1], ['C', 4]],
  'B': [['C', 2], ['D', 5]],
  'C': [['D', 1]],
  'D': []
};

const getNeighbors = (node) => graph[node] || [];

// Find shortest weighted path
const distance = Pathfinding.dijkstra('A', 'D', getNeighbors);
console.log(distance); // 4 (A -> B -> C -> D)

// Get all distances from start
const distances = Pathfinding.dijkstraAll('A', getNeighbors);
console.log(distances.get(JSON.stringify('B'))); // 1
console.log(distances.get(JSON.stringify('C'))); // 3
console.log(distances.get(JSON.stringify('D'))); // 4
```

### Counter2D

2D coordinate counter for frequency analysis and hotspot detection.

#### Constructor

```javascript
const counter = new Counter2D();
```

#### Properties

- `size`: Number of unique positions tracked

#### Methods

**`add(position, count = 1)`**
- Add count to a position
- Parameters:
  - `position`: Position as `[x, y]`, `Point2D`, or `"x,y"` string
  - `count`: Count to add (default: 1)

**`get(position)`**
- Get count at position
- Parameters:
  - `position`: Position in any supported format
- Returns: `number` - Count at position (0 if not found)

**`positionsAboveThreshold(threshold)`**
- Get all positions with count >= threshold
- Parameters:
  - `threshold`: Minimum count (inclusive)
- Returns: `string[]` - Array of position keys "x,y"

**`getMaxCount()`**
- Get the maximum count value
- Returns: `number` - Maximum count, or 0 if empty

**`getMaxPositions()`**
- Get all positions with the maximum count
- Returns: `string[]` - Array of position keys "x,y"

**`forEach(callback)`**
- Execute function for each position-count pair
- Parameters:
  - `callback`: Function receiving (count, position)

**Iteration:**
- Counter2D is iterable with `for...of`, yielding `[position, count]` pairs

#### Example: Track Visited Positions

```javascript
import { Counter2D, Point2D } from './aoc-helpers.js';

const counter = new Counter2D();

// Track visited positions
const path = [[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]];
for (const pos of path) {
  counter.add(pos);
}

console.log(counter.get([0, 0])); // 2 (visited twice)
console.log(counter.get([1, 0])); // 1
console.log(counter.size); // 4 (unique positions)

// Find hotspots (positions visited multiple times)
const hotspots = counter.positionsAboveThreshold(2);
console.log(hotspots); // ['0,0']

// Find most visited position
const maxCount = counter.getMaxCount(); // 2
const maxPositions = counter.getMaxPositions(); // ['0,0']
```

#### Example: Overlapping Lines

```javascript
import { Counter2D } from './aoc-helpers.js';

const counter = new Counter2D();

// Line from (0,0) to (3,0)
for (let x = 0; x <= 3; x++) {
  counter.add([x, 0]);
}

// Line from (1,0) to (1,3)
for (let y = 0; y <= 3; y++) {
  counter.add([1, y]);
}

// Find intersections (positions with count >= 2)
const intersections = counter.positionsAboveThreshold(2);
console.log(intersections); // ['1,0'] (where lines cross)

// Iterate over all counted positions
for (const [pos, count] of counter) {
  console.log(`${pos}: ${count} lines`);
}
```

#### Example: Working with Point2D

```javascript
import { Counter2D, Point2D } from './aoc-helpers.js';

const counter = new Counter2D();
const center = new Point2D(5, 5);

// Add center and all adjacent positions
counter.add(center);
for (const adj of center.adjacentPositions()) {
  counter.add(adj);
}

// All formats work interchangeably
console.log(counter.get([5, 5])); // 1
console.log(counter.get('5,5')); // 1
console.log(counter.get(center)); // 1
```

### MathUtils

Mathematical utility functions.

#### Methods

**`gcd(a, b)`** - Greatest Common Divisor
**`gcdMultiple(...args)`** - GCD of multiple numbers
**`lcm(a, b)`** - Least Common Multiple
**`lcmMultiple(...args)`** - LCM of multiple numbers
**`manhattanDistance(p1, p2)`** - Manhattan distance between [x,y] points
**`sign(x)`** - Sign of number (-1, 0, or 1)

#### Example

```javascript
import { MathUtils } from './aoc-helpers.js';

const gcd = MathUtils.gcd(12, 18);        // 6
const lcm = MathUtils.lcm(12, 18);        // 36
const dist = MathUtils.manhattanDistance([0,0], [3,4]); // 7
```

### AoCUtils

General utility functions.

#### Methods

**`printSolution(part, answer)`** - Standard solution output format
**`chunks(lst, n)`** - Split array into chunks
**`binaryToDecimal(str)`** - Convert binary string to number
**`charToPriority(char)`** - Convert char to priority (a-z: 1-26, A-Z: 27-52)

#### Example

```javascript
import { AoCUtils } from './aoc-helpers.js';

AoCUtils.printSolution(1, 42);  // "Part 1: 42"

const chunks = AoCUtils.chunks([1,2,3,4,5,6], 2); // [[1,2], [3,4], [5,6]]
const num = AoCUtils.binaryToDecimal('1010');     // 10
const priority = AoCUtils.charToPriority('a');    // 1
```

## Usage Examples

### Example 1: Grid Pathfinding

```javascript
import { AoCInput, Grid2D, Point2D, Directions } from './aoc-helpers.js';

const lines = AoCInput.readLines('input.txt');
const grid = new Grid2D(lines);

// Find start position
const startKey = grid.findPositions('S')[0];
const start = Point2D.fromString(startKey);

// BFS using grid and Point2D
const queue = [[start, 0]];
const visited = new Set([start.toString()]);

while (queue.length > 0) {
  const [current, distance] = queue.shift();

  if (grid.get(current) === 'E') {
    console.log('Found exit at distance:', distance);
    break;
  }

  for (const neighbor of current.adjacentPositions(false)) {
    const key = neighbor.toString();
    if (grid.has(neighbor) && !visited.has(key) && grid.get(neighbor) !== '#') {
      visited.add(key);
      queue.push([neighbor, distance + 1]);
    }
  }
}
```

### Example 2: Grid Navigation

```javascript
import { Grid2D, Point2D, Directions } from './aoc-helpers.js';

const grid = new Grid2D(['....', '.##.', '....']);
let pos = new Point2D(0, 0);
let dir = Directions.EAST;

// Simulate robot movement
for (let i = 0; i < 10; i++) {
  const next = pos.add(new Point2D(...dir));

  if (grid.has(next) && grid.get(next) !== '#') {
    pos = next;
  } else {
    dir = Directions.turnRight(dir);
  }
}
```

### Example 3: Counting Adjacent Cells

```javascript
import { Grid2D } from './aoc-helpers.js';

const grid = new Grid2D(['..#', '.##', '...']);

// Count cells adjacent to '#'
let count = 0;
for (const [key, value] of grid) {
  if (value === '#') {
    const adjacent = grid.getAdjacent(key, true);
    count += adjacent.filter(k => grid.get(k) === '.').length;
  }
}
```

## Performance

The library is optimized for AoC-scale problems:

- **Grid2D** uses Map for O(1) lookups with coordinate keys
- **Dimension caching** avoids repeated calculations
- **Sparse grids** only store existing cells (memory efficient)
- **String keys** ("x,y") provide fast Map lookups

Benchmarks on typical hardware:
- **Grid2D:**
  - 1000×1000 grid construction: ~1.5s
  - 10,000 random lookups: ~15ms
  - 10,000 grid iterations: ~2ms
- **Point2D:**
  - 3000 vector operations: <1ms
  - 10,000 string conversions: ~12ms
- **Pathfinding:**
  - BFS on 10,000-node graph: ~30ms
  - BFS-all on 2,500-node graph: ~9ms
  - Dijkstra on 1,000-node graph: ~9ms
  - Dijkstra-all on 900-node graph: ~5ms
- **Counter2D:**
  - 100,000 coordinate updates: ~70ms
  - 50,000 updates to 100 positions: ~30ms
  - Iterate 10,000 entries: ~3ms

See `test/performance.test.js` for detailed benchmarks.
