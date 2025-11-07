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
    """Pathfinding algorithms."""
    
    @staticmethod
    def bfs(
        start: Any,
        goal: Any,
        get_neighbors: Callable[[Any], List[Any]]
    ) -> Optional[List[Any]]:
        """Breadth-first search returning the path."""
        queue = deque([(start, [start])])
        visited = {start}
        
        while queue:
            current, path = queue.popleft()
            
            if current == goal:
                return path
            
            for neighbor in get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    
    @staticmethod
    def bfs_distance(
        start: Any,
        goal: Any,
        get_neighbors: Callable[[Any], List[Any]]
    ) -> Optional[int]:
        """BFS returning just the distance."""
        queue = deque([(start, 0)])
        visited = {start}
        
        while queue:
            current, distance = queue.popleft()
            
            if current == goal:
                return distance
            
            for neighbor in get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, distance + 1))
        
        return None
    
    @staticmethod
    def dijkstra(
        start: Any,
        goal: Any,
        get_neighbors: Callable[[Any], List[Tuple[Any, int]]],
    ) -> Optional[int]:
        """Dijkstra's algorithm returning minimum cost."""
        queue = [(0, start)]
        distances = {start: 0}
        
        while queue:
            current_cost, current = heappop(queue)
            
            if current == goal:
                return current_cost
            
            if current_cost > distances.get(current, float('inf')):
                continue
            
            for neighbor, cost in get_neighbors(current):
                new_cost = current_cost + cost
                
                if new_cost < distances.get(neighbor, float('inf')):
                    distances[neighbor] = new_cost
                    heappush(queue, (new_cost, neighbor))
        
        return None


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