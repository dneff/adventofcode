"""
Advent of Code 2022 - Day 3, Part 2
https://adventofcode.com/2022/day/3

This script finds the common item (badge) in groups of three elves
and sums their priorities.
"""

import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2022/3/input')


def get_unique(a, b, c):
    """
    Find the common item among three rucksacks.

    Args:
        a: First rucksack items
        b: Second rucksack items
        c: Third rucksack items

    Returns:
        str: The common item (badge)
    """
    return set(a).intersection(set(b), set(c)).pop()


def get_value(item):
    """
    Calculate the priority value of an item.
    a-z have values 1-26, A-Z have values 27-52.

    Args:
        item: The item character

    Returns:
        int: Priority value
    """
    value = ord(item)
    value -= 96  # Convert to 1-26 for lowercase
    if value < 0:  # Uppercase letter
        value += 32 + 26
    return value


def solve_part2():
    """
    Find the sum of priorities of badges for each group of three elves.

    Returns:
        int: Sum of badge priorities
    """
    lines = AoCInput.read_lines(INPUT_FILE)
    result = 0

    # Process in groups of 3
    for i in range(0, len(lines), 3):
        badge = get_unique(lines[i], lines[i + 1], lines[i + 2])
        result += get_value(badge)

    return result


# Compute and print the answer for part 2
answer = solve_part2()
AoCUtils.print_solution(2, answer)
