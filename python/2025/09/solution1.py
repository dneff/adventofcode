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

tile_positions = [(int(x), int(y)) for line in AoCInput.read_lines(INPUT_FILE) for x, y in [line.split(',')]]

def get_rectangle_area(pos1, pos2):
    return (abs(pos1[0] - pos2[0]) + 1) * (abs(pos1[1] - pos2[1]) + 1)

def find_largest_rectangle(tile_positions):
    """
    Find the largest rectangle that uses red tiles for two of its opposite corners.
    """
    largest_area = 0
    
    for idx1 in range(len(tile_positions)):
        for idx2 in range(idx1 + 1, len(tile_positions)):
            pos1 = tile_positions[idx1]
            pos2 = tile_positions[idx2]
            if pos1[0] == pos2[0] or pos1[1] == pos2[1]:
                continue
            area = get_rectangle_area(pos1, pos2)
            largest_area = max(largest_area, area)

    return largest_area

AoCUtils.print_solution(1, find_largest_rectangle(tile_positions))
