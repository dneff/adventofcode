"""
Advent of Code 2018 - Day 3: No Matter How You Slice It (Part 2)
https://adventofcode.com/2018/day/3

Find the one claim that doesn't overlap with any other claims.
This is the only claim where all of its square inches are claimed by exactly one claim (itself).

Returns the ID of the non-overlapping claim.
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


def solve_part2():
    """
    Find the ID of the only claim that doesn't overlap with any other claims.

    Returns:
        str: The claim ID that has no overlaps
    """
    claims = AoCInput.read_lines(INPUT_FILE)
    fabric = defaultdict(int)

    # First pass: mark all claimed fabric squares
    for claim_line in claims:
        _, left, top, width, height = parse_claim(claim_line)

        for w in range(width):
            for h in range(height):
                fabric_position = (left + w, top + h)
                fabric[fabric_position] += 1

    # Second pass: find the claim with no overlaps
    for claim_line in claims:
        claim_id, left, top, width, height = parse_claim(claim_line)

        # Check if all squares in this claim are claimed by exactly 1 (no overlaps)
        claim_squares = []
        for w in range(width):
            for h in range(height):
                fabric_position = (left + w, top + h)
                claim_squares.append(fabric[fabric_position] == 1)

        # If all squares are non-overlapping, this is our answer
        if all(claim_squares):
            return claim_id

    return None


# Compute and print the answer for part 2
non_overlapping_claim_id = solve_part2()
AoCUtils.print_solution(2, non_overlapping_claim_id)
