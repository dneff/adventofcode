"""
Advent of Code 2025 - Day 2: Gift Shop
https://adventofcode.com/2025/day/2

--- Part One ---
Find the invalid IDs by looking for any ID which is made only of some 
sequence of digits repeated twice. So, 55 (5 twice), 6464 (64 twice), 
and 123123 (123 twice) would all be invalid IDs.

Find all of the invalid IDs that appear in the given ranges.

What do you get if you add up all of the invalid IDs?
"""

import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2025/2/input')

def find_invalid_ids(start_id: int, end_id: int) -> list[int]:
    """
    Find all invalid IDs in the given range.
    An ID is invalid if it consists of a sequence of digits repeated twice.
    Examples: 55, 6464, 123123.
    """
    found_ids = []
    for current_id in range(start_id, end_id + 1):
        id_str = str(current_id)
        length = len(id_str)
        
        # Only even length strings can be a sequence repeated twice
        if length % 2 == 0:
            midpoint = length // 2
            first_half = id_str[:midpoint]
            second_half = id_str[midpoint:]
            
            # Check if the first half is identical to the second half
            if first_half == second_half:
                found_ids.append(current_id)
                
    return found_ids

# Read the ranges from the input file
raw_ranges = AoCInput.read_lines(INPUT_FILE)[0].split(",")

all_invalid_ids = []
for range_str in raw_ranges:
    range_start, range_end = (int(x) for x in range_str.split("-"))
    all_invalid_ids.extend(find_invalid_ids(range_start, range_end))

AoCUtils.print_solution(1, sum(all_invalid_ids))


