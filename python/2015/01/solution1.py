"""
Advent of Code 2015 - Day 1: Not Quite Lisp
https://adventofcode.com/2015/day/1

This script calculates the final floor Santa ends up on after following the instructions in the input file.
Each '(' means go up one floor, each ')' means go down one floor.
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/1/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils

def solve_part1():
    """
    Reads the input file and computes the final floor based on the instructions.
    '(' increases the floor by 1, ')' decreases the floor by 1.
    Returns:
        int: The final floor Santa ends up on.
    """
    instructions = AoCInput.read_lines(INPUT_FILE)[0]
    floor = 0
    move_map = {
        '(': 1,
        ')': -1
    }

    for char in instructions:
        floor += move_map[char]

    return floor


# Compute and print the answer for part 1
final_floor = solve_part1()
AoCUtils.print_solution(1, final_floor)
