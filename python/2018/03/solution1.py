"""
Advent of Code 2018 - Day 3: No Matter How You Slice It (Part 1)
https://adventofcode.com/2018/day/3

The Elves are making claims on a large fabric square (at least 1000x1000 inches).
Each claim specifies a rectangular area:
- Format: #ID @ left,top: widthxheight
- Example: #123 @ 3,2: 5x4

Count how many square inches of fabric are within two or more claims (overlapping regions).
"""

import os
import sys
from collections import defaultdict
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2018/3/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def parse_claim(claim_line):
    """
    Parse a claim line into its components.

    Args:
        claim_line: String in format "#ID @ left,top: widthxheight"

    Returns:
        tuple: (claim_id, left, top, width, height)
    """
    parts = claim_line.strip().split()
    claim_id = parts[0][1:]  # Remove '#' prefix
    left, top = [int(x) for x in parts[2][:-1].split(',')]  # Remove ':' suffix
    width, height = [int(x) for x in parts[3].split('x')]
    return claim_id, left, top, width, height


def solve_part1():
    """
    Count the number of square inches of fabric claimed by two or more claims.

    Returns:
        int: Number of square inches with overlapping claims
    """
    claims = AoCInput.read_lines(INPUT_FILE)
    fabric = defaultdict(int)

    # Mark all claimed fabric squares
    for claim_line in claims:
        _, left, top, width, height = parse_claim(claim_line)

        # Mark each square inch in this claim
        for w in range(width):
            for h in range(height):
                fabric_position = (left + w, top + h)
                fabric[fabric_position] += 1

    # Count squares claimed by 2 or more
    overlapping_squares = sum(1 for count in fabric.values() if count > 1)
    return overlapping_squares


# Compute and print the answer for part 1
overlapping_inches = solve_part1()
AoCUtils.print_solution(1, overlapping_inches)
