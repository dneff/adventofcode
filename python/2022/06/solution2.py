"""
Advent of Code 2022 - Day 6, Part 2
https://adventofcode.com/2022/day/6

This script finds the first position where 14 consecutive characters are all different.
"""

import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2022/6/input')


def marker_end(s, size=4):
    """
    Find the position after the first sequence of unique characters.

    Args:
        s: Input string
        size: Size of unique sequence to find

    Returns:
        int: Position (1-indexed) after the unique sequence
    """
    marker = []
    for idx, char in enumerate(s):
        marker.append(char)
        if len(marker) < size:
            continue
        if len(marker) > size:
            marker = marker[-size:]
        if len(set(marker)) == size:
            return idx + 1
    raise ValueError("No marker found")


def solve_part2():
    """
    Find the first start-of-message marker (14 unique characters).

    Returns:
        int: Position after the marker
    """
    lines = AoCInput.read_lines(INPUT_FILE)
    return marker_end(lines[0], 14)


# Compute and print the answer for part 2
answer = solve_part2()
AoCUtils.print_solution(2, answer)
