"""
Advent of Code 2022 - Day 4: Camp Cleanup
https://adventofcode.com/2022/day/4

This script counts assignment pairs where one range fully contains the other.
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


def is_subset(a, b):
    """
    Check if one range fully contains the other.

    Args:
        a: First range (min, max)
        b: Second range (min, max)

    Returns:
        bool: True if one range fully contains the other
    """
    # Check if a contains b
    if a[0] <= b[0] and a[1] >= b[1]:
        return True
    # Check if b contains a
    if b[0] <= a[0] and b[1] >= a[1]:
        return True
    return False


def solve_part1():
    """
    Count the number of assignment pairs where one range fully contains the other.

    Returns:
        int: Count of fully overlapping pairs
    """
    lines = AoCInput.read_lines(INPUT_FILE)
    subset_count = 0

    for line in lines:
        min_a, max_a, min_b, max_b = [int(x) for x in re.split(r'[-,]', line)]
        if is_subset((min_a, max_a), (min_b, max_b)):
            subset_count += 1

    return subset_count


# Compute and print the answer for part 1
answer = solve_part1()
AoCUtils.print_solution(1, answer)
