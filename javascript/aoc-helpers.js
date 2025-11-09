/**
 * Advent of Code Helper Classes
 *
 * A comprehensive collection of utilities commonly used across AoC solutions.
 * JavaScript implementation matching Python helper library functionality.
 */

import { readFileSync } from 'fs';

/**
 * Input reading and parsing utilities.
 */
class AoCInput {
  /**
   * Read all lines from file, stripped of whitespace.
   *
   * @param {string} filename - Path to the file to read
   * @param {boolean} [preserveLeadingSpace=false] - If true, only strip trailing whitespace.
   *                                                  If false (default), strip all whitespace.
   * @returns {string[]} List of lines from the file
   * @throws {Error} If file cannot be read
   */
  static readLines(filename, preserveLeadingSpace = false) {
    try {
      const content = readFileSync(filename, 'utf-8');
      const lines = content.split('\n');

      if (preserveLeadingSpace) {
        // Only strip trailing newline and carriage return
        return lines.map((line) => line.replace(/\r?\n?$/, ''));
      } else {
        // Strip all whitespace from both ends
        return lines.map((line) => line.trim());
      }
    } catch (error) {
      throw new Error(`Failed to read file ${filename}: ${error.message}`);
    }
  }

  /**
   * Read file into a 2D grid object with "x,y" string keys mapping to characters.
   *
   * @param {string} filename - Path to the file to read
   * @returns {Object.<string, string>} Grid object with "x,y" keys mapping to character values
   * @throws {Error} If file cannot be read
   */
  static readGrid(filename) {
    try {
      const content = readFileSync(filename, 'utf-8');
      const lines = content.split('\n').map((line) => line.trimEnd());
      const grid = {};

      for (let y = 0; y < lines.length; y++) {
        const line = lines[y];
        for (let x = 0; x < line.length; x++) {
          grid[`${x},${y}`] = line[x];
        }
      }

      return grid;
    } catch (error) {
      throw new Error(`Failed to read grid from ${filename}: ${error.message}`);
    }
  }

  /**
   * Read all integers from file (one per line).
   *
   * @param {string} filename - Path to the file to read
   * @returns {number[]} Array of integers
   * @throws {Error} If file cannot be read or contains non-numeric data
   */
  static readNumbers(filename) {
    try {
      const lines = this.readLines(filename);
      return lines
        .filter((line) => line.length > 0)
        .map((line) => {
          const num = parseInt(line, 10);
          if (isNaN(num)) {
            throw new Error(`Invalid number: ${line}`);
          }
          return num;
        });
    } catch (error) {
      throw new Error(`Failed to read numbers from ${filename}: ${error.message}`);
    }
  }

  /**
   * Read file split by empty lines into sections.
   *
   * @param {string} filename - Path to the file to read
   * @returns {string[][]} Array of sections, each containing an array of lines
   * @throws {Error} If file cannot be read
   */
  static readSections(filename) {
    try {
      const content = readFileSync(filename, 'utf-8').trim();
      return content.split('\n\n').map((section) => section.split('\n'));
    } catch (error) {
      throw new Error(`Failed to read sections from ${filename}: ${error.message}`);
    }
  }

  /**
   * Extract all integers (including negative) from a string.
   *
   * @param {string} text - Text to parse
   * @returns {number[]} Array of integers found in the text
   */
  static parseNumbers(text) {
    const matches = text.match(/-?\d+/g);
    return matches ? matches.map((n) => parseInt(n, 10)) : [];
  }
}

/**
 * Mathematical utilities.
 */
class MathUtils {
  /**
   * Calculate GCD (Greatest Common Divisor) of two numbers using Euclidean algorithm.
   *
   * @param {number} a - First number
   * @param {number} b - Second number
   * @returns {number} GCD of a and b
   */
  static gcd(a, b) {
    a = Math.abs(a);
    b = Math.abs(b);
    while (b !== 0) {
      const temp = b;
      b = a % b;
      a = temp;
    }
    return a;
  }

  /**
   * Calculate GCD of multiple numbers.
   *
   * @param {...number} args - Numbers to find GCD of
   * @returns {number} GCD of all numbers
   * @throws {Error} If no arguments provided
   */
  static gcdMultiple(...args) {
    if (args.length === 0) {
      throw new Error('At least one number required');
    }
    return args.reduce((acc, val) => this.gcd(acc, val));
  }

  /**
   * Calculate LCM (Least Common Multiple) of two numbers.
   *
   * @param {number} a - First number
   * @param {number} b - Second number
   * @returns {number} LCM of a and b
   */
  static lcm(a, b) {
    return Math.abs(a * b) / this.gcd(a, b);
  }

  /**
   * Calculate LCM of multiple numbers.
   *
   * @param {...number} args - Numbers to find LCM of
   * @returns {number} LCM of all numbers
   * @throws {Error} If no arguments provided
   */
  static lcmMultiple(...args) {
    if (args.length === 0) {
      throw new Error('At least one number required');
    }
    return args.reduce((acc, val) => this.lcm(acc, val));
  }

  /**
   * Calculate Manhattan distance between two points.
   *
   * @param {[number, number]} p1 - First point as [x, y]
   * @param {[number, number]} p2 - Second point as [x, y]
   * @returns {number} Manhattan distance
   */
  static manhattanDistance(p1, p2) {
    return Math.abs(p1[0] - p2[0]) + Math.abs(p1[1] - p2[1]);
  }

  /**
   * Return the sign of a number.
   *
   * @param {number} x - Number to get sign of
   * @returns {number} -1 for negative, 0 for zero, 1 for positive
   */
  static sign(x) {
    return x > 0 ? 1 : x < 0 ? -1 : 0;
  }
}

/**
 * General utility functions.
 */
class AoCUtils {
  /**
   * Standard solution printing format.
   *
   * @param {number} part - Part number (1 or 2)
   * @param {*} answer - The answer to print
   */
  static printSolution(part, answer) {
    console.log(`Part ${part}: ${answer}`);
  }

  /**
   * Split array into chunks of size n.
   *
   * @param {Array} lst - Array to chunk
   * @param {number} n - Chunk size
   * @returns {Array[]} Array of chunks
   */
  static chunks(lst, n) {
    const result = [];
    for (let i = 0; i < lst.length; i += n) {
      result.push(lst.slice(i, i + n));
    }
    return result;
  }

  /**
   * Convert binary string to decimal number.
   *
   * @param {string} binaryStr - Binary string (e.g., "1010")
   * @returns {number} Decimal number
   */
  static binaryToDecimal(binaryStr) {
    return parseInt(binaryStr, 2);
  }

  /**
   * Convert character to priority value.
   * Lowercase a-z: 1-26
   * Uppercase A-Z: 27-52
   *
   * @param {string} char - Single character
   * @returns {number} Priority value (0 if not a letter)
   */
  static charToPriority(char) {
    const code = char.charCodeAt(0);
    const aLower = 'a'.charCodeAt(0);
    const zLower = 'z'.charCodeAt(0);
    const aUpper = 'A'.charCodeAt(0);
    const zUpper = 'Z'.charCodeAt(0);

    if (code >= aLower && code <= zLower) {
      return code - aLower + 1;
    } else if (code >= aUpper && code <= zUpper) {
      return code - aUpper + 27;
    }
    return 0;
  }
}

/**
 * 2D coordinate operations with vector arithmetic.
 */
class Point2D {
  /**
   * Create a new Point2D.
   *
   * @param {number} x - X coordinate
   * @param {number} y - Y coordinate
   */
  constructor(x, y) {
    this.x = x;
    this.y = y;
  }

  /**
   * Add another point to this point.
   *
   * @param {Point2D} other - Point to add
   * @returns {Point2D} New point with summed coordinates
   */
  add(other) {
    return new Point2D(this.x + other.x, this.y + other.y);
  }

  /**
   * Subtract another point from this point.
   *
   * @param {Point2D} other - Point to subtract
   * @returns {Point2D} New point with difference
   */
  subtract(other) {
    return new Point2D(this.x - other.x, this.y - other.y);
  }

  /**
   * Check equality with another point.
   *
   * @param {Point2D} other - Point to compare
   * @returns {boolean} True if points have same coordinates
   */
  equals(other) {
    return this.x === other.x && this.y === other.y;
  }

  /**
   * Calculate Manhattan distance to another point.
   *
   * @param {Point2D} other - Target point
   * @returns {number} Manhattan distance
   */
  manhattanDistance(other) {
    return Math.abs(this.x - other.x) + Math.abs(this.y - other.y);
  }

  /**
   * Get adjacent positions (4 or 8 directions).
   *
   * @param {boolean} [includeDiagonals=false] - Include diagonal neighbors
   * @returns {Point2D[]} Array of adjacent points
   */
  adjacentPositions(includeDiagonals = false) {
    const positions = [
      new Point2D(this.x, this.y - 1), // N
      new Point2D(this.x + 1, this.y), // E
      new Point2D(this.x, this.y + 1), // S
      new Point2D(this.x - 1, this.y), // W
    ];

    if (includeDiagonals) {
      positions.push(
        new Point2D(this.x + 1, this.y - 1), // NE
        new Point2D(this.x + 1, this.y + 1), // SE
        new Point2D(this.x - 1, this.y + 1), // SW
        new Point2D(this.x - 1, this.y - 1) // NW
      );
    }

    return positions;
  }

  /**
   * Convert to tuple representation [x, y].
   *
   * @returns {[number, number]} Tuple representation
   */
  toTuple() {
    return [this.x, this.y];
  }

  /**
   * Convert to string representation "x,y".
   *
   * @returns {string} String key for use in Maps/Objects
   */
  toString() {
    return `${this.x},${this.y}`;
  }

  /**
   * Create Point2D from string representation "x,y".
   *
   * @param {string} str - String representation
   * @returns {Point2D} New Point2D instance
   */
  static fromString(str) {
    const [x, y] = str.split(',').map(Number);
    return new Point2D(x, y);
  }
}

/**
 * Direction constants and utilities.
 */
class Directions {
  // Cardinal directions: [dx, dy] where y increases downward
  static NORTH = [0, -1];
  static EAST = [1, 0];
  static SOUTH = [0, 1];
  static WEST = [-1, 0];

  // Direction arrays
  static CARDINAL = [
    [0, -1], // N
    [1, 0], // E
    [0, 1], // S
    [-1, 0], // W
  ];

  static ALL_8 = [
    [0, -1], // N
    [1, -1], // NE
    [1, 0], // E
    [1, 1], // SE
    [0, 1], // S
    [-1, 1], // SW
    [-1, 0], // W
    [-1, -1], // NW
  ];

  // Direction mappings
  static DIRECTION_MAP = {
    N: [0, -1],
    NORTH: [0, -1],
    UP: [0, -1],
    E: [1, 0],
    EAST: [1, 0],
    RIGHT: [1, 0],
    S: [0, 1],
    SOUTH: [0, 1],
    DOWN: [0, 1],
    W: [-1, 0],
    WEST: [-1, 0],
    LEFT: [-1, 0],
  };

  static ARROW_MAP = {
    '^': [0, -1],
    '>': [1, 0],
    v: [0, 1],
    '<': [-1, 0],
  };

  /**
   * Turn 90 degrees clockwise.
   *
   * @param {[number, number]} direction - Current direction [dx, dy]
   * @returns {[number, number]} New direction after turning right
   */
  static turnRight(direction) {
    const [dx, dy] = direction;
    // Normalize -0 to 0 to avoid -0 vs 0 comparison issues
    return [-dy || 0, dx || 0];
  }

  /**
   * Turn 90 degrees counter-clockwise.
   *
   * @param {[number, number]} direction - Current direction [dx, dy]
   * @returns {[number, number]} New direction after turning left
   */
  static turnLeft(direction) {
    const [dx, dy] = direction;
    // Normalize -0 to 0 to avoid -0 vs 0 comparison issues
    return [dy || 0, -dx || 0];
  }
}

/**
 * 2D grid operations and utilities with Map-based storage.
 */
class Grid2D {
  /**
   * Create a new Grid2D.
   *
   * @param {Map<string, string>|Object.<string, string>|string[]} data - Grid data
   *        Can be a Map with "x,y" keys, plain object with "x,y" keys, or array of strings
   */
  constructor(data) {
    this._grid = new Map();
    this._width = null;
    this._height = null;

    if (data instanceof Map) {
      // Copy from Map
      for (const [key, value] of data) {
        this._grid.set(key, value);
      }
    } else if (Array.isArray(data)) {
      // Construct from string array
      for (let y = 0; y < data.length; y++) {
        const line = data[y];
        for (let x = 0; x < line.length; x++) {
          this._grid.set(`${x},${y}`, line[x]);
        }
      }
    } else if (typeof data === 'object') {
      // Copy from plain object
      for (const [key, value] of Object.entries(data)) {
        this._grid.set(key, value);
      }
    }

    // Cache dimensions
    this._calculateDimensions();
  }

  /**
   * Calculate and cache grid dimensions.
   * @private
   */
  _calculateDimensions() {
    if (this._grid.size === 0) {
      this._width = 0;
      this._height = 0;
      return;
    }

    let maxX = 0;
    let maxY = 0;

    for (const key of this._grid.keys()) {
      const [x, y] = key.split(',').map(Number);
      maxX = Math.max(maxX, x);
      maxY = Math.max(maxY, y);
    }

    this._width = maxX + 1;
    this._height = maxY + 1;
  }

  /**
   * Get value at position.
   *
   * @param {number|string|Point2D} x - X coordinate, "x,y" string, or Point2D
   * @param {number} [y] - Y coordinate (if x is a number)
   * @returns {string|undefined} Value at position or undefined if not found
   */
  get(x, y) {
    const key = this._toKey(x, y);
    return this._grid.get(key);
  }

  /**
   * Set value at position.
   *
   * @param {number|string|Point2D} x - X coordinate, "x,y" string, or Point2D
   * @param {number|string} y - Y coordinate (if x is a number) or value (if x is string/Point2D)
   * @param {string} [value] - Value to set (if x and y are numbers)
   */
  set(x, y, value) {
    let key, val;

    if (arguments.length === 2) {
      // set(key, value) or set(Point2D, value)
      key = this._toKey(x);
      val = y;
    } else {
      // set(x, y, value)
      key = this._toKey(x, y);
      val = value;
    }

    this._grid.set(key, val);

    // Update cached dimensions if needed
    const [px, py] = key.split(',').map(Number);
    if (px >= this._width || py >= this._height) {
      this._calculateDimensions();
    }
  }

  /**
   * Check if position exists in grid.
   *
   * @param {number|string|Point2D} x - X coordinate, "x,y" string, or Point2D
   * @param {number} [y] - Y coordinate (if x is a number)
   * @returns {boolean} True if position exists
   */
  has(x, y) {
    const key = this._toKey(x, y);
    return this._grid.has(key);
  }

  /**
   * Delete position from grid.
   *
   * @param {number|string|Point2D} x - X coordinate, "x,y" string, or Point2D
   * @param {number} [y] - Y coordinate (if x is a number)
   * @returns {boolean} True if position was deleted
   */
  delete(x, y) {
    const key = this._toKey(x, y);
    const result = this._grid.delete(key);
    if (result) {
      this._calculateDimensions();
    }
    return result;
  }

  /**
   * Convert position to string key.
   * @private
   * @param {number|string|Point2D} x - X coordinate, "x,y" string, or Point2D
   * @param {number} [y] - Y coordinate (if x is a number)
   * @returns {string} Key string "x,y"
   */
  _toKey(x, y) {
    if (typeof x === 'string') {
      return x;
    } else if (x instanceof Point2D) {
      return x.toString();
    } else {
      return `${x},${y}`;
    }
  }

  /**
   * Get grid dimensions.
   *
   * @returns {{width: number, height: number}} Grid dimensions
   */
  getDimensions() {
    return { width: this._width, height: this._height };
  }

  /**
   * Get width of grid.
   *
   * @returns {number} Grid width
   */
  get width() {
    return this._width;
  }

  /**
   * Get height of grid.
   *
   * @returns {number} Grid height
   */
  get height() {
    return this._height;
  }

  /**
   * Get size (number of cells) in grid.
   *
   * @returns {number} Number of cells
   */
  get size() {
    return this._grid.size;
  }

  /**
   * Get adjacent positions that exist in the grid.
   *
   * @param {number|string|Point2D} x - X coordinate, "x,y" string, or Point2D
   * @param {number} [y] - Y coordinate (if x is a number)
   * @param {boolean} [includeDiagonals=false] - Include diagonal neighbors
   * @returns {string[]} Array of adjacent position keys
   */
  getAdjacent(x, y, includeDiagonals = false) {
    // Handle overloaded parameters
    let px, py, diagonals;
    if (typeof y === 'boolean') {
      // getAdjacent(key, includeDiagonals) or getAdjacent(Point2D, includeDiagonals)
      const key = this._toKey(x);
      [px, py] = key.split(',').map(Number);
      diagonals = y;
    } else {
      // getAdjacent(x, y, includeDiagonals)
      px = x;
      py = y;
      diagonals = includeDiagonals;
    }

    const adjacent = [];
    const directions = diagonals ? Directions.ALL_8 : Directions.CARDINAL;

    for (const [dx, dy] of directions) {
      const newKey = `${px + dx},${py + dy}`;
      if (this._grid.has(newKey)) {
        adjacent.push(newKey);
      }
    }

    return adjacent;
  }

  /**
   * Find all positions containing a specific value.
   *
   * @param {string} value - Value to search for
   * @returns {string[]} Array of position keys
   */
  findPositions(value) {
    const positions = [];
    for (const [key, val] of this._grid) {
      if (val === value) {
        positions.push(key);
      }
    }
    return positions;
  }

  /**
   * Check if position is within grid bounds.
   *
   * @param {number|string|Point2D} x - X coordinate, "x,y" string, or Point2D
   * @param {number} [y] - Y coordinate (if x is a number)
   * @returns {boolean} True if position is in bounds
   */
  inBounds(x, y) {
    return this.has(x, y);
  }

  /**
   * Print grid to console for debugging.
   */
  printGrid() {
    if (this._grid.size === 0) {
      console.log('(empty grid)');
      return;
    }

    for (let y = 0; y < this._height; y++) {
      let line = '';
      for (let x = 0; x < this._width; x++) {
        line += this._grid.get(`${x},${y}`) || ' ';
      }
      console.log(line);
    }
  }

  /**
   * Iterate over all positions and values.
   *
   * @returns {Iterator<[string, string]>} Iterator of [key, value] pairs
   */
  *entries() {
    yield* this._grid.entries();
  }

  /**
   * Iterate over all position keys.
   *
   * @returns {Iterator<string>} Iterator of position keys
   */
  *keys() {
    yield* this._grid.keys();
  }

  /**
   * Iterate over all values.
   *
   * @returns {Iterator<string>} Iterator of values
   */
  *values() {
    yield* this._grid.values();
  }

  /**
   * Make Grid2D iterable (iterates over entries).
   *
   * @returns {Iterator<[string, string]>} Iterator of [key, value] pairs
   */
  [Symbol.iterator]() {
    return this._grid.entries();
  }

  /**
   * Execute a function for each position in the grid.
   *
   * @param {Function} callback - Function to execute for each entry (value, key, grid)
   */
  forEach(callback) {
    this._grid.forEach((value, key) => callback(value, key, this));
  }
}

/**
 * Priority queue implementation using binary min-heap.
 * Used internally for Dijkstra's algorithm.
 * @private
 */
class MinHeap {
  constructor() {
    this._heap = [];
  }

  /**
   * Add element to heap.
   *
   * @param {number} priority - Priority value (lower is higher priority)
   * @param {*} value - Value to store
   */
  push(priority, value) {
    this._heap.push({ priority, value });
    this._bubbleUp(this._heap.length - 1);
  }

  /**
   * Remove and return element with lowest priority.
   *
   * @returns {{priority: number, value: *}|null} Element with lowest priority or null if empty
   */
  pop() {
    if (this._heap.length === 0) return null;
    if (this._heap.length === 1) return this._heap.pop();

    const min = this._heap[0];
    this._heap[0] = this._heap.pop();
    this._bubbleDown(0);
    return min;
  }

  /**
   * Get size of heap.
   *
   * @returns {number} Number of elements
   */
  get size() {
    return this._heap.length;
  }

  /**
   * Bubble element up to maintain heap property.
   * @private
   */
  _bubbleUp(index) {
    while (index > 0) {
      const parentIndex = Math.floor((index - 1) / 2);
      if (this._heap[index].priority >= this._heap[parentIndex].priority) break;

      [this._heap[index], this._heap[parentIndex]] = [this._heap[parentIndex], this._heap[index]];
      index = parentIndex;
    }
  }

  /**
   * Bubble element down to maintain heap property.
   * @private
   */
  _bubbleDown(index) {
    while (true) {
      const leftChild = 2 * index + 1;
      const rightChild = 2 * index + 2;
      let smallest = index;

      if (
        leftChild < this._heap.length &&
        this._heap[leftChild].priority < this._heap[smallest].priority
      ) {
        smallest = leftChild;
      }

      if (
        rightChild < this._heap.length &&
        this._heap[rightChild].priority < this._heap[smallest].priority
      ) {
        smallest = rightChild;
      }

      if (smallest === index) break;

      [this._heap[index], this._heap[smallest]] = [this._heap[smallest], this._heap[index]];
      index = smallest;
    }
  }
}

/**
 * Pathfinding algorithms for graph traversal.
 */
class Pathfinding {
  /**
   * Breadth-first search returning the complete path from start to goal.
   *
   * @param {*} start - Starting position
   * @param {*} goal - Goal position
   * @param {Function} getNeighbors - Function that takes a position and returns array of neighbors
   * @returns {Array|null} Path from start to goal (inclusive) or null if no path exists
   *
   * @example
   * const path = Pathfinding.bfs(
   *   [0, 0],
   *   [3, 3],
   *   (pos) => getValidNeighbors(pos)
   * );
   */
  static bfs(start, goal, getNeighbors) {
    const queue = [[start, [start]]];
    const visited = new Set();
    visited.add(JSON.stringify(start));

    while (queue.length > 0) {
      const [current, path] = queue.shift();

      if (JSON.stringify(current) === JSON.stringify(goal)) {
        return path;
      }

      for (const neighbor of getNeighbors(current)) {
        const neighborKey = JSON.stringify(neighbor);
        if (!visited.has(neighborKey)) {
          visited.add(neighborKey);
          queue.push([neighbor, [...path, neighbor]]);
        }
      }
    }

    return null;
  }

  /**
   * Breadth-first search returning only the distance to the goal.
   *
   * @param {*} start - Starting position
   * @param {*} goal - Goal position
   * @param {Function} getNeighbors - Function that takes a position and returns array of neighbors
   * @returns {number} Distance from start to goal, or -1 if no path exists
   *
   * @example
   * const distance = Pathfinding.bfsDistance(
   *   [0, 0],
   *   [3, 3],
   *   (pos) => getValidNeighbors(pos)
   * );
   */
  static bfsDistance(start, goal, getNeighbors) {
    const queue = [[start, 0]];
    const visited = new Set();
    visited.add(JSON.stringify(start));

    while (queue.length > 0) {
      const [current, distance] = queue.shift();

      if (JSON.stringify(current) === JSON.stringify(goal)) {
        return distance;
      }

      for (const neighbor of getNeighbors(current)) {
        const neighborKey = JSON.stringify(neighbor);
        if (!visited.has(neighborKey)) {
          visited.add(neighborKey);
          queue.push([neighbor, distance + 1]);
        }
      }
    }

    return -1;
  }

  /**
   * Breadth-first search returning distances to all reachable positions.
   *
   * @param {*} start - Starting position
   * @param {Function} getNeighbors - Function that takes a position and returns array of neighbors
   * @returns {Map<string, number>} Map of JSON-stringified positions to their distances from start
   *
   * @example
   * const distances = Pathfinding.bfsAll(
   *   [0, 0],
   *   (pos) => getValidNeighbors(pos)
   * );
   * console.log(distances.get(JSON.stringify([2, 3]))); // Distance to [2, 3]
   */
  static bfsAll(start, getNeighbors) {
    const queue = [[start, 0]];
    const distances = new Map();
    distances.set(JSON.stringify(start), 0);

    while (queue.length > 0) {
      const [current, distance] = queue.shift();

      for (const neighbor of getNeighbors(current)) {
        const neighborKey = JSON.stringify(neighbor);
        if (!distances.has(neighborKey)) {
          distances.set(neighborKey, distance + 1);
          queue.push([neighbor, distance + 1]);
        }
      }
    }

    return distances;
  }

  /**
   * Dijkstra's algorithm for weighted graphs, returning shortest distance to goal.
   *
   * @param {*} start - Starting position
   * @param {*} goal - Goal position
   * @param {Function} getNeighbors - Function that takes a position and returns array of [neighbor, cost] tuples
   * @returns {number|null} Shortest distance to goal, or null if no path exists
   *
   * @example
   * const distance = Pathfinding.dijkstra(
   *   [0, 0],
   *   [3, 3],
   *   (pos) => getNeighborsWithCosts(pos) // Returns [[neighbor1, cost1], [neighbor2, cost2], ...]
   * );
   */
  static dijkstra(start, goal, getNeighbors) {
    const heap = new MinHeap();
    heap.push(0, start);
    const distances = new Map();
    distances.set(JSON.stringify(start), 0);

    while (heap.size > 0) {
      const { priority: currentCost, value: current } = heap.pop();
      const currentKey = JSON.stringify(current);

      if (currentKey === JSON.stringify(goal)) {
        return currentCost;
      }

      // Skip if we've found a better path already
      if (currentCost > (distances.get(currentKey) ?? Infinity)) {
        continue;
      }

      for (const [neighbor, cost] of getNeighbors(current)) {
        const newCost = currentCost + cost;
        const neighborKey = JSON.stringify(neighbor);

        if (newCost < (distances.get(neighborKey) ?? Infinity)) {
          distances.set(neighborKey, newCost);
          heap.push(newCost, neighbor);
        }
      }
    }

    return null;
  }

  /**
   * Dijkstra's algorithm returning distances to all reachable positions.
   *
   * @param {*} start - Starting position
   * @param {Function} getNeighbors - Function that takes a position and returns array of [neighbor, cost] tuples
   * @returns {Map<string, number>} Map of JSON-stringified positions to their distances from start
   *
   * @example
   * const distances = Pathfinding.dijkstraAll(
   *   [0, 0],
   *   (pos) => getNeighborsWithCosts(pos)
   * );
   * console.log(distances.get(JSON.stringify([2, 3]))); // Shortest distance to [2, 3]
   */
  static dijkstraAll(start, getNeighbors) {
    const heap = new MinHeap();
    heap.push(0, start);
    const distances = new Map();
    distances.set(JSON.stringify(start), 0);

    while (heap.size > 0) {
      const { priority: currentCost, value: current } = heap.pop();
      const currentKey = JSON.stringify(current);

      // Skip if we've found a better path already
      if (currentCost > (distances.get(currentKey) ?? Infinity)) {
        continue;
      }

      for (const [neighbor, cost] of getNeighbors(current)) {
        const newCost = currentCost + cost;
        const neighborKey = JSON.stringify(neighbor);

        if (newCost < (distances.get(neighborKey) ?? Infinity)) {
          distances.set(neighborKey, newCost);
          heap.push(newCost, neighbor);
        }
      }
    }

    return distances;
  }
}

/**
 * 2D coordinate counter for frequency analysis.
 */
class Counter2D {
  /**
   * Create a new Counter2D.
   */
  constructor() {
    this._counts = new Map();
  }

  /**
   * Add count to a position.
   *
   * @param {[number, number]|Point2D|string} position - Position as [x, y], Point2D, or "x,y" string
   * @param {number} [count=1] - Count to add (default: 1)
   *
   * @example
   * const counter = new Counter2D();
   * counter.add([3, 4]);
   * counter.add([3, 4], 5);
   */
  add(position, count = 1) {
    const key = this._toKey(position);
    this._counts.set(key, (this._counts.get(key) ?? 0) + count);
  }

  /**
   * Get count at a position.
   *
   * @param {[number, number]|Point2D|string} position - Position as [x, y], Point2D, or "x,y" string
   * @returns {number} Count at position (0 if position not found)
   *
   * @example
   * const count = counter.get([3, 4]);
   */
  get(position) {
    const key = this._toKey(position);
    return this._counts.get(key) ?? 0;
  }

  /**
   * Get all positions with count above threshold.
   *
   * @param {number} threshold - Minimum count (inclusive)
   * @returns {string[]} Array of position keys "x,y" with count >= threshold
   *
   * @example
   * const hotspots = counter.positionsAboveThreshold(10);
   */
  positionsAboveThreshold(threshold) {
    const positions = [];
    for (const [key, count] of this._counts) {
      if (count >= threshold) {
        positions.push(key);
      }
    }
    return positions;
  }

  /**
   * Get the maximum count value.
   *
   * @returns {number} Maximum count, or 0 if counter is empty
   *
   * @example
   * const max = counter.getMaxCount();
   */
  getMaxCount() {
    if (this._counts.size === 0) return 0;
    return Math.max(...this._counts.values());
  }

  /**
   * Get all positions with the maximum count.
   *
   * @returns {string[]} Array of position keys "x,y" with maximum count
   *
   * @example
   * const maxPositions = counter.getMaxPositions();
   */
  getMaxPositions() {
    const maxCount = this.getMaxCount();
    if (maxCount === 0) return [];

    const positions = [];
    for (const [key, count] of this._counts) {
      if (count === maxCount) {
        positions.push(key);
      }
    }
    return positions;
  }

  /**
   * Convert position to string key.
   * @private
   * @param {[number, number]|Point2D|string} position - Position in any supported format
   * @returns {string} Key string "x,y"
   */
  _toKey(position) {
    if (typeof position === 'string') {
      return position;
    } else if (position instanceof Point2D) {
      return position.toString();
    } else if (Array.isArray(position)) {
      return `${position[0]},${position[1]}`;
    }
    throw new Error('Invalid position format');
  }

  /**
   * Iterate over all position-count pairs.
   *
   * @returns {Iterator<[string, number]>} Iterator of [position, count] pairs
   *
   * @example
   * for (const [pos, count] of counter) {
   *   console.log(`${pos}: ${count}`);
   * }
   */
  *[Symbol.iterator]() {
    yield* this._counts.entries();
  }

  /**
   * Get number of unique positions.
   *
   * @returns {number} Number of positions tracked
   */
  get size() {
    return this._counts.size;
  }

  /**
   * Execute a function for each position-count pair.
   *
   * @param {Function} callback - Function to execute for each entry (count, position)
   */
  forEach(callback) {
    this._counts.forEach((count, position) => callback(count, position));
  }
}

export { AoCInput, MathUtils, AoCUtils, Point2D, Directions, Grid2D, Pathfinding, Counter2D };
