"""
Advent of Code 2022 - Day 12: Hill Climbing Algorithm (Part 2)
https://adventofcode.com/2022/day/12

Find the shortest path from any position at height 'a' to the end (E),
searching backwards from E to find the closest 'a' position.
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
    Perform BFS searching backwards from end to find shortest downhill path to height 'a'.

    Args:
        start: Starting position (x, y) - the end point E
        end: Ending position (x, y) - any position at height 'a'
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
            # Stop when we reach any position at height 'a'
            if heights[grid[(x, y)]] == heights[grid[end]]:
                return len(path) - 1

            for location in get_adjacent((x, y), grid):
                location_height = heights[grid[location]]
                # Going downhill: can descend at most one level
                if current_height - location_height <= 1:
                    new_path = path[:]
                    new_path.append(location)
                    queue.append(new_path)


def solve_part2():
    """
    Find the shortest path from any 'a' position to E by searching backwards from E.

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

    # Search backwards from E to any 'a' position (including S which is also 'a')
    return breadth_search(end, start, grid)


# Compute and print the answer for part 2
answer = solve_part2()
AoCUtils.print_solution(2, answer)
