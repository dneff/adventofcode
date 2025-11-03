"""
Advent of Code 2017 - Day 2: Corruption Checksum (Part 2)

Calculate the sum of each row's result where you divide the only two numbers that evenly divide
each other. In each row, there are exactly two numbers where one evenly divides the other.

Example:
    5 9 2 8  -> 8 divides by 2 = 4
    9 4 7 3  -> 9 divides by 3 = 3
    3 8 6 5  -> 6 divides by 3 = 2
    Sum: 4 + 3 + 2 = 9
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/2/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def find_evenly_divisible_quotient(row_values):
    """
    Find the quotient of the two numbers in the row where one evenly divides the other.

    Args:
        row_values: List of integers in the row

    Returns:
        The quotient of the two evenly divisible numbers
    """
    # Sort in descending order to always divide larger by smaller
    sorted_values = sorted(row_values, reverse=True)

    for i, larger in enumerate(sorted_values):
        for smaller in sorted_values[i+1:]:
            if larger % smaller == 0:
                return larger // smaller

    return 0


def main():
    """Calculate the divisible checksum for the spreadsheet."""
    lines = AoCInput.read_lines(INPUT_FILE)
    row_quotients = []

    for row in lines:
        row_values = [int(x) for x in row.split()]
        row_quotients.append(find_evenly_divisible_quotient(row_values))

    checksum = sum(row_quotients)
    AoCUtils.print_solution(2, checksum)


if __name__ == "__main__":
    main()
