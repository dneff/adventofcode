"""
Advent of Code 2018 - Day 2: Inventory Management System (Part 2)
https://adventofcode.com/2018/day/2

Find the two box IDs that differ by exactly one character at the same position.
Return the common letters between these two IDs (excluding the differing character).

This helps identify prototype fabric boxes that are likely stored together.
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2018/2/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def solve_part2():
    """
    Find two box IDs differing by exactly one character and return common letters.

    Returns:
        str: The common letters between the two matching box IDs
    """
    box_ids = [line.strip() for line in AoCInput.read_lines(INPUT_FILE)]
    seen_ids = []

    for box_id in box_ids:
        # Compare with all previously seen IDs
        for seen_id in seen_ids:
            # Count positions where characters differ
            mismatches = sum(1 for char1, char2 in zip(box_id, seen_id) if char1 != char2)

            # If exactly one character differs, we found the match
            if mismatches == 1:
                # Extract common letters (where characters match)
                common_letters = ''.join(char1 for char1, char2 in zip(box_id, seen_id) if char1 == char2)
                return common_letters

        seen_ids.append(box_id)

    return None


# Compute and print the answer for part 2
common_letters = solve_part2()
AoCUtils.print_solution(2, common_letters)
