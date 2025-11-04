"""
Advent of Code 2018 - Day 2: Inventory Management System (Part 1)
https://adventofcode.com/2018/day/2

Calculate a checksum for a list of box IDs by counting:
1. How many box IDs contain a letter which appears exactly twice
2. How many box IDs contain a letter which appears exactly three times
3. Multiply these two counts together

Example: If 4 IDs have letters appearing exactly twice and 3 IDs have letters
appearing exactly three times, the checksum is 4 × 3 = 12.
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2018/2/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def solve_part1():
    """
    Calculate the checksum by counting box IDs with repeated letters.

    Returns:
        int: The checksum (count of IDs with doubles × count of IDs with triples)
    """
    box_ids = AoCInput.read_lines(INPUT_FILE)
    ids_with_doubles = set()
    ids_with_triples = set()

    for box_id in box_ids:
        box_id = box_id.strip()

        # Check each character in the box ID
        for char in box_id:
            char_count = box_id.count(char)

            # Track IDs with exactly 2 or 3 of any letter
            if char_count == 2:
                ids_with_doubles.add(box_id)
            elif char_count == 3:
                ids_with_triples.add(box_id)

    # Calculate checksum by multiplying the counts
    checksum = len(ids_with_doubles) * len(ids_with_triples)
    return checksum


# Compute and print the answer for part 1
checksum = solve_part1()
AoCUtils.print_solution(1, checksum)
