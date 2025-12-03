"""
Advent of Code 2025 - Day 2: Gift Shop
https://adventofcode.com/2025/day/2

--- Part Two ---
Now, an ID is invalid if it is made only of some sequence of digits repeated 
at least twice. So, 12341234 (1234 two times), 123123123 (123 three times), 
1212121212 (12 five times), and 1111111 (1 seven times) are all invalid IDs.

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
    An ID is invalid if it is made only of some sequence of digits 
    repeated at least twice.
    Examples: 12341234, 123123123, 1111111.
    """
    found_ids = []
    for current_id in range(start_id, end_id + 1):
        id_str = str(current_id)
        length = len(id_str)
        
        # Check possible sequence lengths from 1 up to half the string length
        for seq_length in range(1, length // 2 + 1):
            # The total length must be a multiple of the sequence length
            if length % seq_length == 0:
                sequence = id_str[:seq_length]
                repetitions = length // seq_length
                
                # Check if repeating this sequence reconstructs the original ID
                if sequence * repetitions == id_str:
                    found_ids.append(current_id)
                    break  # Found a valid repetition pattern, move to next ID
                
    return found_ids

# Read the ranges from the input file
raw_ranges = AoCInput.read_lines(INPUT_FILE)[0].split(",")

all_invalid_ids = []
for range_str in raw_ranges:
    range_start, range_end = (int(x) for x in range_str.split("-"))
    all_invalid_ids.extend(find_invalid_ids(range_start, range_end))

AoCUtils.print_solution(2, sum(all_invalid_ids))


