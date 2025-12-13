"""
Advent of Code Helper Classes

A comprehensive collection of utilities commonly used across AoC solutions.
Consolidates patterns found in 300+ solutions from 2015-2024.
"""

import re
from collections import defaultdict, deque, Counter
from heapq import heappush, heappop
from math import gcd
from functools import reduce
from typing import List, Dict, Tuple, Set, Optional, Union, Callable, Any


class AoCInput:
    """Input reading and parsing utilities."""
    
    @staticmethod
    def read_lines(filename: str, preserve_leading_space: bool = False) -> List[str]:
        """Read all lines from file, stripped of whitespace.

        Args:
            filename: Path to the file to read
            preserve_leading_space: If True, only strip trailing whitespace (rstrip).
                                   If False (default), strip all whitespace (strip).

        Returns:
            List of lines from the file
        """
        with open(filename, "r", encoding="utf-8") as f:
            if preserve_leading_space:
                return [line.rstrip('\n') for line in f.readlines()]
            else:
                return [line.strip() for line in f.readlines()]
    
    @staticmethod
    def read_grid(filename: str) -> Dict[Tuple[int, int], str]:
        """Read file into a 2D grid dictionary with (x, y) coordinates."""
        grid = {}
        with open(filename, "r", encoding="utf-8") as f:
            for y, line in enumerate(f.readlines()):
                for x, char in enumerate(line.strip()):
                    grid[(x, y)] = char
        return grid
    
    @staticmethod
    def read_numbers(filename: str) -> List[int]:
        """Read all integers from file."""
        with open(filename, "r", encoding="utf-8") as f:
            return [int(line.strip()) for line in f.readlines()]
    
    @staticmethod
    def read_file(filename: str) -> str:
        """Read entire file as a single string.

        Args:
            filename: Path to the file to read

        Returns:
            File contents as a string
        """
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def read_sections(filename: str) -> List[List[str]]:
        """Read file split by empty lines into sections."""
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read().strip()
        return [section.split('\n') for section in content.split('\n\n')]

    @staticmethod
    def parse_numbers(text: str) -> List[int]:
        """Extract all integers from a string."""
        return [int(x) for x in re.findall(r'-?\d+', text)]


class Point2D:
    """2D coordinate operations."""
    
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def __add__(self, other: 'Point2D') -> 'Point2D':
        return Point2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Point2D') -> 'Point2D':
        return Point2D(self.x - other.x, self.y - other.y)
    
    def __eq__(self, other: 'Point2D') -> bool:
        return self.x == other.x and self.y == other.y
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def __repr__(self) -> str:
        return f"Point2D({self.x}, {self.y})"
    
    def manhattan_distance(self, other: 'Point2D') -> int:
        """Calculate Manhattan distance to another point."""
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    def adjacent_positions(self, include_diagonals: bool = False) -> List['Point2D']:
        """Get adjacent positions (4 or 8 directions)."""
        positions = [
            Point2D(self.x, self.y + 1),  # N
            Point2D(self.x + 1, self.y),  # E
            Point2D(self.x, self.y - 1),  # S
            Point2D(self.x - 1, self.y),  # W
        ]
        
        if include_diagonals:
            positions.extend([
                Point2D(self.x + 1, self.y + 1),  # NE
                Point2D(self.x + 1, self.y - 1),  # SE
                Point2D(self.x - 1, self.y + 1),  # NW
                Point2D(self.x - 1, self.y - 1),  # SW
            ])
        
        return positions
    
    def to_tuple(self) -> Tuple[int, int]:
        """Convert to tuple representation."""
        return (self.x, self.y)


class Grid2D:
    """2D grid operations and utilities."""
    
    def __init__(self, data: Union[Dict[Tuple[int, int], str], List[str]]):
        if isinstance(data, list):
            self.grid = {}
            for y, line in enumerate(data):
                for x, char in enumerate(line):
                    self.grid[(x, y)] = char
        else:
            self.grid = data.copy()
    
    def __getitem__(self, pos: Tuple[int, int]) -> str:
        return self.grid.get(pos, '')
    
    def __setitem__(self, pos: Tuple[int, int], value: str):
        self.grid[pos] = value
    
    def __contains__(self, pos: Tuple[int, int]) -> bool:
        return pos in self.grid
    
    def get_dimensions(self) -> Tuple[int, int]:
        """Get grid dimensions (width, height)."""
        if not self.grid:
            return (0, 0)
        
        max_x = max(pos[0] for pos in self.grid.keys())
        max_y = max(pos[1] for pos in self.grid.keys())
        return (max_x + 1, max_y + 1)
    
    def get_adjacent(self, pos: Tuple[int, int], include_diagonals: bool = False) -> List[Tuple[int, int]]:
        """Get adjacent positions that exist in the grid."""
        x, y = pos
        adjacent = []
        
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # N, E, S, W
        if include_diagonals:
            directions.extend([(1, 1), (1, -1), (-1, 1), (-1, -1)])  # NE, SE, NW, SW
        
        for dx, dy in directions:
            new_pos = (x + dx, y + dy)
            if new_pos in self.grid:
                adjacent.append(new_pos)
        
        return adjacent
    
    def find_positions(self, value: str) -> List[Tuple[int, int]]:
        """Find all positions containing a specific value."""
        return [pos for pos, val in self.grid.items() if val == value]
    
    def in_bounds(self, pos: Tuple[int, int]) -> bool:
        """Check if position is within grid bounds."""
        return pos in self.grid
    
    def print_grid(self):
        """Print the grid for debugging."""
        if not self.grid:
            return
        
        width, height = self.get_dimensions()
        for y in range(height):
            line = ""
            for x in range(width):
                line += self.grid.get((x, y), ' ')
            print(line)


class Directions:
    """Direction constants and utilities."""
    
    CARDINAL = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # N, S, E, W
    ALL_8 = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
    
    DIRECTION_MAP = {
        "N": (0, -1), "NORTH": (0, -1), "UP": (0, -1),
        "E": (1, 0), "EAST": (1, 0), "RIGHT": (1, 0),
        "S": (0, 1), "SOUTH": (0, 1), "DOWN": (0, 1),
        "W": (-1, 0), "WEST": (-1, 0), "LEFT": (-1, 0),
    }
    
    ARROW_MAP = {
        "^": (0, -1), ">": (1, 0), "v": (0, 1), "<": (-1, 0)
    }
    
    @staticmethod
    def turn_right(direction: Tuple[int, int]) -> Tuple[int, int]:
        """Turn 90 degrees clockwise."""
        dx, dy = direction
        return (-dy, dx)
    
    @staticmethod
    def turn_left(direction: Tuple[int, int]) -> Tuple[int, int]:
        """Turn 90 degrees counter-clockwise."""
        dx, dy = direction
        return (dy, -dx)


class Pathfinding:
    """
    Graph pathfinding and search algorithms for Advent of Code problems.

    This class provides implementations of common pathfinding algorithms optimized
    for grid-based puzzles, graph traversal, and shortest path problems. All methods
    are generic and work with any hashable node type (tuples, strings, custom objects).

    Typical use cases:
    - Finding shortest paths in 2D/3D grids
    - Graph traversal with uniform or weighted edges
    - Maze solving and navigation problems
    - State space exploration
    """

    @staticmethod
    def bfs_with_path(
        start_node: Any,
        goal_node: Any,
        get_neighbors_fn: Callable[[Any], List[Any]]
    ) -> Optional[List[Any]]:
        """
        Breadth-First Search that returns the complete path from start to goal.

        BFS explores nodes level by level, guaranteeing the shortest path when all
        edges have equal weight (unweighted graph). This variant tracks and returns
        the full path, making it suitable when you need to know the route taken.

        Algorithm characteristics:
        - Time complexity: O(V + E) where V is vertices and E is edges
        - Space complexity: O(V) for the visited set and queue
        - Guarantees shortest path in unweighted graphs
        - Explores nodes in order of increasing distance from start

        Args:
            start_node: The starting position/state (any hashable type)
            goal_node: The target position/state to reach
            get_neighbors_fn: Function that takes a node and returns list of
                            adjacent/reachable nodes. Should only return valid,
                            traversable neighbors (pre-filtered for walls, bounds, etc.)

        Returns:
            List representing the path from start to goal (inclusive), or None if
            no path exists. The path includes both start_node and goal_node.

        Example:
            >>> def neighbors(pos):
            ...     x, y = pos
            ...     return [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]
            >>> path = Pathfinding.bfs_with_path((0,0), (3,3), neighbors)
            >>> print(path)  # [(0,0), (1,0), (2,0), (3,0), (3,1), (3,2), (3,3)]
        """
        # Queue stores tuples of (current_node, path_to_current)
        # Starting path contains only the start node
        search_queue = deque([(start_node, [start_node])])
        visited_nodes = {start_node}

        while search_queue:
            current_node, path_to_current = search_queue.popleft()

            # Goal check: return the complete path when we reach the target
            if current_node == goal_node:
                return path_to_current

            # Explore all unvisited neighbors
            for adjacent_node in get_neighbors_fn(current_node):
                if adjacent_node not in visited_nodes:
                    visited_nodes.add(adjacent_node)
                    # Extend the path with this neighbor
                    path_to_neighbor = path_to_current + [adjacent_node]
                    search_queue.append((adjacent_node, path_to_neighbor))

        # No path exists from start to goal
        return None

    @staticmethod
    def bfs_distance(
        start_node: Any,
        goal_node: Any,
        get_neighbors_fn: Callable[[Any], List[Any]]
    ) -> Optional[int]:
        """
        Breadth-First Search that returns only the shortest distance (step count).

        This is a memory-optimized variant of BFS that only tracks distance instead
        of the full path. Use this when you only need to know how far apart two nodes
        are, not the actual route between them. Significantly more memory-efficient
        than bfs_with_path for large search spaces.

        Algorithm characteristics:
        - Time complexity: O(V + E) where V is vertices and E is edges
        - Space complexity: O(V) for the visited set and queue
        - More memory efficient than tracking full paths
        - Returns the minimum number of steps (edges) from start to goal

        Args:
            start_node: The starting position/state (any hashable type)
            goal_node: The target position/state to reach
            get_neighbors_fn: Function that takes a node and returns list of
                            adjacent/reachable nodes. Should only return valid,
                            traversable neighbors (pre-filtered for walls, bounds, etc.)

        Returns:
            Integer representing the minimum number of steps from start to goal,
            or None if no path exists. Distance of 0 means start equals goal.

        Example:
            >>> def neighbors(pos):
            ...     x, y = pos
            ...     return [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]
            >>> dist = Pathfinding.bfs_distance((0,0), (3,3), neighbors)
            >>> print(dist)  # 6 (Manhattan distance in this case)
        """
        # Queue stores tuples of (current_node, steps_from_start)
        search_queue = deque([(start_node, 0)])
        visited_nodes = {start_node}

        while search_queue:
            current_node, steps_from_start = search_queue.popleft()

            # Goal check: return the distance when we reach the target
            if current_node == goal_node:
                return steps_from_start

            # Explore all unvisited neighbors at distance + 1
            for adjacent_node in get_neighbors_fn(current_node):
                if adjacent_node not in visited_nodes:
                    visited_nodes.add(adjacent_node)
                    search_queue.append((adjacent_node, steps_from_start + 1))

        # No path exists from start to goal
        return None

    @staticmethod
    def dijkstra(
        start_node: Any,
        goal_node: Any,
        get_neighbors_with_cost_fn: Callable[[Any], List[Tuple[Any, int]]],
    ) -> Optional[int]:
        """
        Dijkstra's algorithm for finding the minimum cost path in weighted graphs.

        This algorithm finds the shortest path when edges have different costs/weights.
        It uses a priority queue to always explore the lowest-cost path first, guaranteeing
        an optimal solution for graphs with non-negative edge weights. Essential for
        problems where movement has variable costs.

        Algorithm characteristics:
        - Time complexity: O((V + E) log V) with binary heap
        - Space complexity: O(V) for the distance map and priority queue
        - Guarantees optimal path with non-negative edge weights
        - More general than BFS (BFS is Dijkstra with all edge weights = 1)
        - Does NOT work correctly with negative edge weights (use Bellman-Ford instead)

        Args:
            start_node: The starting position/state (any hashable type)
            goal_node: The target position/state to reach
            get_neighbors_with_cost_fn: Function that takes a node and returns a list of
                                       (neighbor_node, edge_cost) tuples. Edge costs must
                                       be non-negative. Only return valid neighbors.

        Returns:
            Integer representing the minimum total cost to reach goal from start,
            or None if no path exists. Cost of 0 means start equals goal.

        Example:
            >>> def neighbors_with_cost(pos):
            ...     x, y = pos
            ...     # Moving right/down costs 1, left/up costs 2
            ...     result = []
            ...     result.append(((x+1, y), 1))  # right
            ...     result.append(((x, y+1), 1))  # down
            ...     result.append(((x-1, y), 2))  # left
            ...     result.append(((x, y-1), 2))  # up
            ...     return result
            >>> cost = Pathfinding.dijkstra((0,0), (3,3), neighbors_with_cost)
            >>> print(cost)  # 6 (three right moves + three down moves)
        """
        # Priority queue stores tuples of (cost_to_node, node)
        # Heap is ordered by cost, ensuring we always process lowest cost first
        priority_queue = [(0, start_node)]

        # Track the minimum known cost to reach each node
        # Once we pop a node from the queue, we've found its optimal cost
        shortest_costs = {start_node: 0}

        while priority_queue:
            cost_to_current, current_node = heappop(priority_queue)

            # Goal check: return cost when we reach the target
            # Since we process lowest costs first, this is guaranteed optimal
            if current_node == goal_node:
                return cost_to_current

            # Skip if we've already found a better path to this node
            # This happens when the same node is added to the queue multiple times
            if cost_to_current > shortest_costs.get(current_node, float('inf')):
                continue

            # Explore all neighbors and update costs
            for adjacent_node, edge_cost in get_neighbors_with_cost_fn(current_node):
                # Calculate total cost to reach neighbor via current node
                cost_via_current = cost_to_current + edge_cost

                # Only update if we found a better (cheaper) path
                if cost_via_current < shortest_costs.get(adjacent_node, float('inf')):
                    shortest_costs[adjacent_node] = cost_via_current
                    heappush(priority_queue, (cost_via_current, adjacent_node))

        # No path exists from start to goal
        return None

    # Maintain backward compatibility with old function name
    @staticmethod
    def bfs(
        start: Any,
        goal: Any,
        get_neighbors: Callable[[Any], List[Any]]
    ) -> Optional[List[Any]]:
        """
        Deprecated: Use bfs_with_path instead for clarity.

        This is a compatibility alias that calls bfs_with_path.
        """
        return Pathfinding.bfs_with_path(start, goal, get_neighbors)


class MathUtils:
    """Mathematical utilities."""
    
    @staticmethod
    def divisors(n: int) -> List[int]:
        """Return all divisors of n."""
        divs = set()
        for i in range(1, int(n**0.5) + 1):
            if n % i == 0:
                divs.add(i)
                divs.add(n // i)
        return sorted(divs)
    
    @staticmethod
    def gcd_multiple(*args: int) -> int:
        """GCD of multiple numbers."""
        return reduce(gcd, args)
    
    @staticmethod
    def lcm(a: int, b: int) -> int:
        """LCM of two numbers."""
        return abs(a * b) // gcd(a, b)
    
    @staticmethod
    def lcm_multiple(*args: int) -> int:
        """LCM of multiple numbers."""
        return reduce(MathUtils.lcm, args)
    
    @staticmethod
    def manhattan_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
        """Manhattan distance between two points."""
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
    @staticmethod
    def sign(x: int) -> int:
        """Return the sign of a number (-1, 0, or 1)."""
        return (x > 0) - (x < 0)


class Counter2D:
    """2D coordinate counter for frequency analysis."""
    
    def __init__(self):
        self.counts = defaultdict(int)
    
    def add(self, pos: Tuple[int, int], count: int = 1):
        """Add count to position."""
        self.counts[pos] += count
    
    def get(self, pos: Tuple[int, int]) -> int:
        """Get count at position."""
        return self.counts[pos]
    
    def positions_with_count(self, target_count: int) -> List[Tuple[int, int]]:
        """Get all positions with specific count."""
        return [pos for pos, count in self.counts.items() if count == target_count]
    
    def positions_above_threshold(self, threshold: int) -> List[Tuple[int, int]]:
        """Get all positions with count above threshold."""
        return [pos for pos, count in self.counts.items() if count >= threshold]


class AoCUtils:
    """General utility functions."""
    
    @staticmethod
    def print_solution(part: int, answer: Any):
        """Standard solution printing format."""
        print(f"Part {part}: {answer}")
    
    @staticmethod
    def chunks(lst: List[Any], n: int) -> List[List[Any]]:
        """Split list into chunks of size n."""
        return [lst[i:i + n] for i in range(0, len(lst), n)]
    
    @staticmethod
    def binary_to_decimal(binary_str: str) -> int:
        """Convert binary string to decimal."""
        return int(binary_str, 2)
    
    @staticmethod
    def char_to_priority(char: str) -> int:
        """Convert character to priority (a-z: 1-26, A-Z: 27-52)."""
        if 'a' <= char <= 'z':
            return ord(char) - ord('a') + 1
        elif 'A' <= char <= 'Z':
            return ord(char) - ord('A') + 27
        return 0

    @staticmethod
    def ocr_screen_4x6(screen):
        """
        OCR for 6-row tall capital letters (4 pixels wide with 1 pixel spacing).
        Returns the recognized text string.

        Args:
            screen: Either a list of strings, a list of lists of characters,
                   or a multi-line string. Should contain 6 rows of characters.
        """
        # Letter patterns (6 rows x 4 columns, using # for lit pixels, . for off)
        patterns = {
            'A': [
                '.##.',
                '#..#',
                '#..#',
                '####',
                '#..#',
                '#..#'
            ],
            'B': [
                '###.',
                '#..#',
                '###.',
                '#..#',
                '#..#',
                '###.'
            ],
            'C': [
                '.##.',
                '#..#',
                '#...',
                '#...',
                '#..#',
                '.##.'
            ],
            'E': [
                '####',
                '#...',
                '###.',
                '#...',
                '#...',
                '####'
            ],
            'F': [
                '####',
                '#...',
                '###.',
                '#...',
                '#...',
                '#...'
            ],
            'G': [
                '.##.',
                '#..#',
                '#...',
                '#.##',
                '#..#',
                '.###'
            ],
            'H': [
                '#..#',
                '#..#',
                '####',
                '#..#',
                '#..#',
                '#..#'
            ],
            'J': [
                '..##',
                '...#',
                '...#',
                '...#',
                '#..#',
                '.##.'
            ],
            'K': [
                '#..#',
                '#.#.',
                '##..',
                '#.#.',
                '#.#.',
                '#..#'
            ],
            'L': [
                '#...',
                '#...',
                '#...',
                '#...',
                '#...',
                '####'
            ],
            'P': [
                '###.',
                '#..#',
                '#..#',
                '###.',
                '#...',
                '#...'
            ],
            'R': [
                '###.',
                '#..#',
                '#..#',
                '###.',
                '#.#.',
                '#..#'
            ],
            'S': [
                '.###',
                '#...',
                '#...',
                '.##.',
                '...#',
                '###.'
            ],
            'U': [
                '#..#',
                '#..#',
                '#..#',
                '#..#',
                '#..#',
                '.##.'
            ],
            'Z': [
                '####',
                '...#',
                '..#.',
                '.#..',
                '#...',
                '####'
            ]
        }

        # Normalize input to list of strings
        if isinstance(screen, str):
            # Multi-line string - split by newlines and filter out empty/label lines
            lines = screen.split('\n')
            screen_str = []
            for line in lines:
                # Skip lines that don't look like image data (e.g., "The image is:")
                if line and any(c in line for c in ['#', '.', ' ']):
                    # Check if this line has enough content to be an image row
                    if '#' in line or line.count('.') > 3 or line.count(' ') > 3:
                        screen_str.append(line)
        elif isinstance(screen, list):
            if len(screen) > 0 and isinstance(screen[0], list):
                # List of lists - join each row
                screen_str = [''.join(row) for row in screen]
            else:
                # List of strings - use as is
                screen_str = list(screen)
        else:
            raise ValueError("Screen must be a string, list of strings, or list of lists")

        # Ensure we have exactly 6 rows
        if len(screen_str) != 6:
            raise ValueError(f"Expected 6 rows for OCR, got {len(screen_str)}")

        # Find the minimum leading spaces across all rows to preserve alignment
        min_leading_spaces = float('inf')
        for row in screen_str:
            if row.strip():  # Only count non-empty rows
                leading_spaces = len(row) - len(row.lstrip(' '))
                min_leading_spaces = min(min_leading_spaces, leading_spaces)

        # Remove the common leading spaces from all rows
        if min_leading_spaces != float('inf') and min_leading_spaces > 0:
            screen_str = [row[min_leading_spaces:] if len(row) > min_leading_spaces else row
                         for row in screen_str]

        # Strip trailing spaces from all rows
        screen_str = [row.rstrip() for row in screen_str]

        # Normalize all rows to use '.' for off pixels instead of spaces
        screen_str = [row.replace(' ', '.') for row in screen_str]

        result = ''
        x = 0
        while x < len(screen_str[0]):
            # Extract 4-column slice for this letter
            letter_slice = []
            for row in screen_str:
                if x + 3 < len(row):
                    letter_slice.append(row[x:x+4])
                else:
                    letter_slice.append(row[x:].ljust(4, '.'))

            # Match against patterns
            found = False
            for letter, pattern in patterns.items():
                match = True
                for i in range(6):
                    if letter_slice[i] != pattern[i]:
                        match = False
                        break
                if match:
                    result += letter
                    found = True
                    break

            if not found and any('#' in row for row in letter_slice):
                result += '?'

            x += 5  # Move to next letter (4 pixels + 1 space)

        return result