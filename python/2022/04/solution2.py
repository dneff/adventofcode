"""
Advent of Code 2022 - Day 4, Part 2
https://adventofcode.com/2022/day/4

This script counts assignment pairs where ranges overlap at all.
"""

import os
import sys
import re

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2022/4/input')


def is_overlapping(a, b):
    """
    Check if two ranges overlap at all.

    Args:
        a: First range (min, max)
        b: Second range (min, max)

    Returns:
        bool: True if ranges overlap
    """
    # Check if any endpoint of a is in b
    for x in a:
        if b[0] <= x <= b[1]:
            return True
    # Check if any endpoint of b is in a
    for x in b:
        if a[0] <= x <= a[1]:
            return True
    return False


def solve_part2():
    """
    Count the number of assignment pairs where ranges overlap at all.

    Returns:
        int: Count of overlapping pairs
    """
    lines = AoCInput.read_lines(INPUT_FILE)
    overlap_count = 0

    for line in lines:
        min_a, max_a, min_b, max_b = [int(x) for x in re.split(r'[-,]', line)]
        if is_overlapping((min_a, max_a), (min_b, max_b)):
            overlap_count += 1

    return overlap_count


# Compute and print the answer for part 2
answer = solve_part2()
AoCUtils.print_solution(2, answer)
