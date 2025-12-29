"""
Advent of Code 2022 - Day 3: Rucksack Reorganization
https://adventofcode.com/2022/day/3

This script finds the common item in each rucksack's two compartments
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


def get_unique(a, b):
    """
    Find the common item between two compartments.

    Args:
        a: First compartment items
        b: Second compartment items

    Returns:
        str: The common item
    """
    return set(a).intersection(set(b)).pop()


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


def solve_part1():
    """
    Find the sum of priorities of common items in each rucksack.

    Returns:
        int: Sum of priorities
    """
    lines = AoCInput.read_lines(INPUT_FILE)
    result = 0

    for line in lines:
        middle = len(line) // 2
        a, b = line[:middle], line[middle:]
        common_item = get_unique(a, b)
        result += get_value(common_item)

    return result


# Compute and print the answer for part 1
answer = solve_part1()
AoCUtils.print_solution(1, answer)
