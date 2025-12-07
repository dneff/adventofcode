"""
Advent of Code 2025 - Day 5: Cafeteria
https://adventofcode.com/2025/day/5

The database operates on ingredient IDs. It consists of a list of
fresh ingredient ID ranges, a blank line, and a list of available ingredient IDs.

Part 1

Process the database file from the new inventory management system. How many
of the available ingredient IDs are fresh?

"""

import os
import sys
from itertools import accumulate, islice

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "../../"))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, "../../../../aoc-data/2025/5/input")


def parse_input(input_data):
    """
    Parse the ingredient database file into fresh ranges and available IDs.

    The input consists of two sections separated by a blank line:
    1. Fresh ingredient ID ranges in format "start-end" (inclusive)
    2. Available ingredient IDs to check (one per line)

    Args:
        input_data: List of lines from the input file

    Returns:
        Tuple of (fresh_ranges, available_ids) where:
        - fresh_ranges: List of (start, end) tuples representing fresh ID ranges
        - available_ids: List of ingredient IDs to check for freshness
    """
    fresh_ranges = []
    available_ids = []
    is_fresh_section = True

    for line in input_data:
        line = line.strip()
        # Blank line separates fresh ranges from available IDs
        if line == "":
            is_fresh_section = False
            continue
        if is_fresh_section:
            # Parse range format "start-end" (e.g., "3-5" means IDs 3, 4, 5 are fresh)
            start, end = map(int, line.split("-"))
            fresh_ranges.append((start, end))
        else:
            # Parse individual available ingredient IDs
            available_ids.append(int(line))

    return fresh_ranges, available_ids


fresh_ranges, available_ids = parse_input(AoCInput.read_lines(INPUT_FILE))


def check_ranges_overlap(range_a, range_b):
    """
    Check if two ranges overlap or touch each other.

    Two ranges overlap if they share any values or are adjacent.
    For example: (1,3) and (3,5) overlap because they share 3.

    Args:
        range_a: Tuple of (start, end) representing first range
        range_b: Tuple of (start, end) representing second range

    Returns:
        True if ranges overlap or touch, False otherwise
    """
    return not (range_a[1] < range_b[0] or range_b[1] < range_a[0])


def is_ingredient_fresh(ingredient_id, fresh_ranges):
    """
    Check if an ingredient ID falls within any of the fresh ranges.

    An ingredient is fresh if it's within at least one fresh range (inclusive).

    Args:
        ingredient_id: The ID to check
        fresh_ranges: List of (start, end) tuples representing fresh ID ranges

    Returns:
        True if the ingredient ID is within any fresh range, False otherwise
    """
    for start, end in fresh_ranges:
        if start <= ingredient_id <= end:
            return True
    return False


def is_ingredient_fresh(ingredient_id, fresh_ranges):
    """
    Check if an ingredient ID falls within any of the fresh ranges.

    An ingredient is fresh if it's within at least one fresh range (inclusive).

    Args:
        ingredient_id: The ID to check
        fresh_ranges: List of (start, end) tuples representing fresh ID ranges

    Returns:
        True if the ingredient ID is within any fresh range, False otherwise
    """
    for start, end in fresh_ranges:
        if start <= ingredient_id <= end:
            return True
    return False


# Consolidate overlapping ranges to optimize freshness checking
# This reduces the number of ranges we need to check against each ingredient ID
found_overlaps = True
merged_ranges = []
ranges_to_skip = set()

while found_overlaps:
    found_overlaps = False

    # Check all pairs of ranges for overlaps
    for i in range(len(fresh_ranges)):
        if i in ranges_to_skip:
            continue

        for j in range(i + 1, len(fresh_ranges)):
            if j in ranges_to_skip:
                continue

            # If ranges overlap, merge them into a single larger range
            if check_ranges_overlap(fresh_ranges[i], fresh_ranges[j]):
                merged_start = min(fresh_ranges[i][0], fresh_ranges[j][0])
                merged_end = max(fresh_ranges[i][1], fresh_ranges[j][1])
                merged_ranges.append((merged_start, merged_end))

                # Mark both ranges as processed (they've been merged)
                ranges_to_skip.add(i)
                ranges_to_skip.add(j)
                found_overlaps = True

    # Keep unmerged ranges and add newly merged ones
    fresh_ranges = [
        r for idx, r in enumerate(fresh_ranges) if idx not in ranges_to_skip
    ] + merged_ranges

    # Reset for next iteration
    merged_ranges = []
    ranges_to_skip.clear()

# Count how many how many ingredient IDs are fresh
fresh_count = sum(
    1 for ingredient_id in available_ids if is_ingredient_fresh(ingredient_id, fresh_ranges)
)


AoCUtils.print_solution(1, fresh_count)
