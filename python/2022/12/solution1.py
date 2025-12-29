"""
Advent of Code 2022 - Day 12: Hill Climbing Algorithm
https://adventofcode.com/2022/day/12

Find the shortest path from start (S) to end (E) on a heightmap,
where you can only move to positions at most one height level higher.
"""

import os
import sys
from string import ascii_lowercase
from collections import deque

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2022/12/input')


def get_adjacent(pos, grid):
    """
    Find valid adjacent positions in the grid.

    Args:
        pos: Current position as (x, y) tuple
        grid: Dictionary mapping positions to characters

    Returns:
        List of valid adjacent positions
    """
    possible = [
        (pos[0] + 1, pos[1]),
        (pos[0] - 1, pos[1]),
        (pos[0], pos[1] + 1),
        (pos[0], pos[1] - 1)
    ]
    return [x for x in possible if x in grid]


def breadth_search(start, end, grid):
    """
    Perform BFS to find shortest uphill path from start to end.

    Args:
        start: Starting position (x, y)
        end: Ending position (x, y)
        grid: Dictionary mapping positions to height characters

    Returns:
        Length of shortest path, or None if no path exists
    """
    heights = {c: ord(c) for c in ascii_lowercase}
    heights["S"] = ord("a")
    heights["E"] = ord("z")

    queue, seen = deque(), set()
    queue.append([start])

    while queue:
        path = queue.popleft()
        x, y = path[-1]
        current_height = heights[grid[(x, y)]]

        if (x, y) not in seen:
            seen.add((x, y))
            if (x, y) == end:
                return len(path) - 1

            for location in get_adjacent((x, y), grid):
                location_height = heights[grid[location]]
                if location_height <= current_height + 1:
                    new_path = path[:]
                    new_path.append(location)
                    queue.append(new_path)


def solve_part1():
    """
    Find the shortest path from S to E on the heightmap.

    Returns:
        int: The minimum number of steps required
    """
    lines = AoCInput.read_lines(INPUT_FILE)

    grid = {}
    start = ()
    end = ()

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            grid[(x, y)] = char
            if char == "S":
                start = (x, y)
            if char == "E":
                end = (x, y)

    return breadth_search(start, end, grid)


# Compute and print the answer for part 1
answer = solve_part1()
AoCUtils.print_solution(1, answer)
