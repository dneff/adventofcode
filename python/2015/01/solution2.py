"""
Advent of Code 2015 - Day 1, Part 2
https://adventofcode.com/2015/day/1

This script finds the position of the first character in the input that causes Santa to enter the basement (floor -1).
"""

import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_PATH = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/1/input')


def find_basement_entry_position():
    """
    Returns the position (1-based index) of the first character that causes Santa to enter the basement.
    """
    instructions = AoCInput.read_lines(INPUT_PATH)[0]
    current_floor = 0
    move_map = {'(': 1, ')': -1}

    for idx, char in enumerate(instructions):
        current_floor += move_map[char]
        if current_floor == -1:
            return idx + 1


# Compute and print the solution for Part 2
solution = find_basement_entry_position()
AoCUtils.print_solution(2, solution)
