"""
Advent of Code 2022 - Day 14: Regolith Reservoir (Part 2)
https://adventofcode.com/2022/day/14

Simulate falling sand with an infinite floor two units below the lowest rock.
Count how many units of sand come to rest before the source is blocked.
"""

import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2022/14/input')


def generate_cave(lines):
    """
    Parse input and generate cave map with rock formations.

    Args:
        lines: List of input lines describing rock paths

    Returns:
        dict: Cave map where keys are (x, y) positions and values are '#' for rock
    """
    cave = {}
    rock = "#"

    for line in lines:
        locations = line.strip().split(" -> ")
        locations = [
            (int(x.split(",")[0]), int(x.split(",")[1])) for x in locations
        ]
        for idx in range(len(locations) - 1):
            start, end = locations[idx], locations[idx + 1]
            if start[0] == end[0]:
                # Vertical line
                x = start[0]
                for y in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
                    cave[(x, y)] = rock
            else:
                # Horizontal line
                y = start[1]
                for x in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
                    cave[(x, y)] = rock

    return cave


def add_sand(cave, depth):
    """
    Add a grain of sand to the cave and simulate its fall with a floor.

    Sand falls down, then down-left, then down-right until it comes to rest
    or reaches the floor.

    Args:
        cave: Cave map dictionary
        depth: Floor depth - sand stops falling here

    Returns:
        bool: True if sand can still be added, False if source is blocked
    """
    fill_point = (500, 0)
    pos = fill_point

    while pos[1] < depth:
        new_depth = pos[1] + 1
        left, middle, right = (
            (pos[0] - 1, new_depth),
            (pos[0], new_depth),
            (pos[0] + 1, new_depth),
        )

        # Try to move down
        if middle not in cave.keys():
            pos = middle
        # Try to move down-left
        elif left not in cave.keys():
            pos = left
        # Try to move down-right
        elif right not in cave.keys():
            pos = right
        # Can't move - sand comes to rest
        else:
            cave[pos] = "o"
            # Check if source is blocked
            if pos == fill_point:
                return False
            return True

    # Sand reached the floor
    cave[pos] = "o"
    return True


def solve_part2():
    """
    Simulate falling sand with a floor until the source is blocked.

    Returns:
        int: Number of units of sand that come to rest
    """
    lines = AoCInput.read_lines(INPUT_FILE)
    cave = generate_cave(lines)

    # Floor is two units below the lowest rock
    floor = max([x[1] for x in cave.keys()]) + 2

    # Keep adding sand until source is blocked
    filling = True
    while filling:
        filling = add_sand(cave, floor - 1)

    # Count resting sand (all non-rock positions)
    resting_sand = sum([1 for x in cave.values() if x != "#"])

    return resting_sand


# Compute and print the answer for part 2
answer = solve_part2()
AoCUtils.print_solution(2, answer)
