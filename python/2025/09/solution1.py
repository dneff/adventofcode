"""
Advent of Code 2025 - Day 9: Movie Theater
https://adventofcode.com/2025/day/9

The movie theater has a big tile floor with an interesting pattern. Elves 
here are redecorating the theater by switching out some of the square tiles 
in the big grid they form. Some of the tiles are red; the Elves would like 
to find the largest rectangle that uses red tiles for two of its opposite 
corners. They even have a list of where the red tiles are located in the 
grid (your puzzle input).

Part 1
Using two red tiles as opposite corners, what is the largest area of any rectangle you can make?

"""

import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "../../"))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, "../../../../aoc-data/2025/9/input")

# Parse input: each line contains "x,y" coordinates of a red tile
red_tile_positions = [
    (int(x), int(y))
    for line in AoCInput.read_lines(INPUT_FILE)
    for x, y in [line.split(',')]
]


def calculate_rectangle_area(corner1, corner2):
    """
    Calculate the area of a rectangle defined by two opposite corners.

    The +1 accounts for inclusive coordinates (tiles at both corners are included).
    For example, corners at (2,3) and (5,7) give:
    - Width: |5-2| + 1 = 4 tiles
    - Height: |7-3| + 1 = 5 tiles
    - Area: 4 * 5 = 20 tiles

    Args:
        corner1: Tuple (x, y) representing first corner position
        corner2: Tuple (x, y) representing second corner position

    Returns:
        Integer area in number of tiles
    """
    width = abs(corner1[0] - corner2[0]) + 1
    height = abs(corner1[1] - corner2[1]) + 1
    return width * height


def find_largest_rectangle(red_tile_positions):
    """
    Find the largest rectangle that uses red tiles as opposite corners.

    Strategy:
    - Try all pairs of red tiles as potential opposite corners
    - Skip pairs that share the same x or y coordinate (not opposite corners)
    - Calculate area for each valid rectangle
    - Return the maximum area found

    Args:
        red_tile_positions: List of (x, y) tuples representing red tile locations

    Returns:
        Integer representing the largest rectangle area in tiles
    """
    largest_area = 0

    # Try all pairs of red tiles
    for idx1 in range(len(red_tile_positions)):
        for idx2 in range(idx1 + 1, len(red_tile_positions)):
            corner1 = red_tile_positions[idx1]
            corner2 = red_tile_positions[idx2]

            # Skip if tiles are aligned horizontally or vertically
            # (they can't be opposite corners of a rectangle)
            if corner1[0] == corner2[0] or corner1[1] == corner2[1]:
                continue

            # Calculate area and track the maximum
            area = calculate_rectangle_area(corner1, corner2)
            largest_area = max(largest_area, area)

    return largest_area


AoCUtils.print_solution(1, find_largest_rectangle(red_tile_positions))
