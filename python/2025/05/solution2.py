"""
Advent of Code 2025 - Day 5: Cafeteria
https://adventofcode.com/2025/day/5

The database operates on ingredient IDs. It consists of a list of
fresh ingredient ID ranges, a blank line, and a list of available ingredient IDs.

Part 2

Instead of checking which available IDs are fresh, count the total number
of ingredient IDs that are considered fresh according to the fresh ranges.
This is the sum of all IDs within the consolidated fresh ranges.

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

    For Part 2, we only need the fresh ranges to count total fresh IDs,
    but we still parse the available IDs for consistency.

    Args:
        input_data: List of lines from the input file

    Returns:
        Tuple of (fresh_ranges, available_ids) where:
        - fresh_ranges: List of (start, end) tuples representing fresh ID ranges
        - available_ids: List of ingredient IDs (not used in Part 2)
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


# Consolidate overlapping ranges to simplify counting
# By merging overlapping ranges, we can accurately count total fresh IDs
# without double-counting any IDs that appear in multiple ranges
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

# Part 2: Count the total number of fresh ingredient IDs
# After consolidating ranges, we can sum up the size of each range
# For a range (start, end), the count is (end - start + 1) since ranges are inclusive
# Example: range (3, 5) contains IDs 3, 4, 5 = 3 IDs total
total_fresh_ids = sum(end - start + 1 for start, end in fresh_ranges)

AoCUtils.print_solution(2, total_fresh_ids)
