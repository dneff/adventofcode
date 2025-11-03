"""
Advent of Code 2017 - Day 17: Spinlock (Part 2)

Find the value after 0 in the buffer after 50 million insertions. Building the actual
buffer would be too slow and memory-intensive.

Key optimization: Value 0 always stays at position 0 (nothing is ever inserted before it).
We only need to track what value is at position 1, since that's the value after 0.

Instead of maintaining the full buffer, we:
1. Track the current position and buffer size
2. When an insertion would place a value at position 1, record it
3. Continue until 50 million insertions are complete
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/17/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def find_value_after_zero(step_size, num_insertions):
    """
    Find the value at position 1 (after 0) without building the full buffer.

    Args:
        step_size: Number of steps to move forward each iteration
        num_insertions: Number of values to insert

    Returns:
        Value that would be at position 1 after all insertions
    """
    current_position = 0
    buffer_size = 1
    value_after_zero = 0

    for value in range(1, num_insertions + 1):
        # Calculate new position after stepping
        current_position = (current_position + step_size) % buffer_size

        # Increment buffer size (we're about to insert)
        buffer_size += 1

        # Move to newly inserted position
        current_position += 1

        # If we inserted at position 1, track this value
        if current_position == 1:
            value_after_zero = value

    return value_after_zero


def main():
    """Find value after 0 after 50 million insertions."""
    step_size = 328
    num_insertions = 50000000

    result = find_value_after_zero(step_size, num_insertions)
    AoCUtils.print_solution(2, result)


if __name__ == "__main__":
    main()
