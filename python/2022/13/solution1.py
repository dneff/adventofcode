"""
Advent of Code 2022 - Day 13: Distress Signal
https://adventofcode.com/2022/day/13

Compare pairs of packet data (nested lists) to determine which pairs are in the right order.
Sum the indices of correctly ordered pairs.
"""

import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2022/13/input')


def compare(left, right):
    """
    Compare two packet values according to the distress signal protocol.

    If both are integers:
        - If left < right, return 1 (correct order)
        - If left > right, return -1 (wrong order)
        - Otherwise, return 0 (continue checking)

    If both are lists:
        - Compare element by element
        - If left runs out first, return 1 (correct order)
        - If right runs out first, return -1 (wrong order)
        - Otherwise, return 0 (continue checking)

    If exactly one is an integer:
        - Convert integer to list and retry comparison

    Args:
        left: Left packet value (int or list)
        right: Right packet value (int or list)

    Returns:
        int: -1 (wrong order), 0 (equal/unknown), 1 (correct order)
    """
    FALSE = -1
    UNKNOWN = 0
    TRUE = 1

    # Both are integers
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return TRUE
        elif left > right:
            return FALSE
        return UNKNOWN

    # Both are lists
    if isinstance(left, list) and isinstance(right, list):
        while len(left) != 0:
            if len(right) == 0:
                return FALSE
            test = compare(left.pop(0), right.pop(0))
            if test != UNKNOWN:
                return test

        if len(right) != 0:
            return TRUE
        return UNKNOWN

    # One is integer, one is list - convert integer to list
    if isinstance(left, int):
        left = [left]
    if isinstance(right, int):
        right = [right]

    return compare(left, right)


def solve_part1():
    """
    Compare pairs of packets and sum indices of correctly ordered pairs.

    Returns:
        int: Sum of 1-based indices of correctly ordered pairs
    """
    lines = AoCInput.read_lines(INPUT_FILE)

    result = 0
    idx = 0
    i = 0

    while i < len(lines):
        idx += 1

        # Read pair of packets
        left = eval(lines[i])
        right = eval(lines[i + 1])

        # Check if pair is in correct order
        comp = compare(left, right)
        if comp == 1:
            result += idx

        # Skip blank line and move to next pair
        i += 3

    return result


# Compute and print the answer for part 1
answer = solve_part1()
AoCUtils.print_solution(1, answer)
