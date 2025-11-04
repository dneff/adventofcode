"""
Advent of Code 2018 - Day 1: Chronal Calibration (Part 1)
https://adventofcode.com/2018/day/1

Starting with a frequency of zero, apply a sequence of frequency changes to determine
the resulting frequency. Each change is either positive (+X) or negative (-X).

Example: +1, -2, +3, +1 yields a final frequency of 3 (0+1-2+3+1 = 3)
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2018/1/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def solve_part1():
    """
    Calculate the resulting frequency after applying all frequency changes.

    Returns:
        int: The final frequency after all changes have been applied
    """
    frequency_changes = AoCInput.read_lines(INPUT_FILE)
    current_frequency = 0

    # Apply each frequency change
    for change in frequency_changes:
        current_frequency += int(change.strip())

    return current_frequency


# Compute and print the answer for part 1
final_frequency = solve_part1()
AoCUtils.print_solution(1, final_frequency)
