"""
Advent of Code 2019 - Day 17: Set and Forget - Part 1

Run the ASCII program to get a view of scaffolding and a vacuum robot. Find all
scaffold intersections (where scaffolds cross) and calculate the sum of their
alignment parameters (x * y coordinates).
"""
import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402
from IntCode import IntCode, OutputInterrupt  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/17/input')


def is_intersection(grid, x, y):
    """
    Check if position is an intersection (scaffold in all 4 directions).

    Args:
        grid: 2D list of characters
        x, y: Position to check

    Returns:
        True if intersection, False otherwise
    """
    adjacent_positions = [
        grid[y + 1][x], grid[y - 1][x],
        grid[y][x + 1], grid[y][x - 1],
        grid[y][x]
    ]
    return all(char == '#' for char in adjacent_positions)


def solve_part1():
    """Find sum of alignment parameters for all intersections."""
    program = AoCInput.read_file(INPUT_FILE).strip()

    camera_computer = IntCode(program)
    camera_computer.complete = False

    # Collect camera view
    camera_output = []
    while not camera_computer.complete:
        try:
            camera_computer.run()
        except OutputInterrupt:
            ascii_value = chr(int(camera_computer.pop()))
            camera_output.append(ascii_value)

    # Parse into grid
    view_string = ''.join(camera_output).strip()
    grid = [[char for char in line] for line in view_string.split('\n')]

    # Find all intersections
    intersections = []
    for y in range(1, len(grid) - 2):
        for x in range(1, len(grid[y]) - 1):
            if grid[y][x] == '#' and is_intersection(grid, x, y):
                intersections.append((x, y))

    # Calculate sum of alignment parameters
    alignment_sum = sum(x * y for x, y in intersections)
    return alignment_sum


answer = solve_part1()
AoCUtils.print_solution(1, answer)
