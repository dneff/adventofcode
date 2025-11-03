"""
Advent of Code 2017 - Day 2: Corruption Checksum (Part 1)

Calculate the spreadsheet's checksum by finding the difference between the largest and smallest
values in each row, then summing all these differences.

Example:
    5 1 9 5  -> max=9, min=1, difference=8
    7 5 3    -> max=7, min=3, difference=4
    2 4 6 8  -> max=8, min=2, difference=6
    Checksum: 8 + 4 + 6 = 18
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/2/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def calculate_row_difference(row_values):
    """
    Calculate the difference between the maximum and minimum values in a row.

    Args:
        row_values: List of integers in the row

    Returns:
        Difference between max and min values
    """
    return max(row_values) - min(row_values)


def main():
    """Calculate the corruption checksum for the spreadsheet."""
    lines = AoCInput.read_lines(INPUT_FILE)
    row_differences = []

    for row in lines:
        row_values = [int(x) for x in row.split()]
        row_differences.append(calculate_row_difference(row_values))

    checksum = sum(row_differences)
    AoCUtils.print_solution(1, checksum)


if __name__ == "__main__":
    main()
