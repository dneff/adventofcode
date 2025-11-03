"""
Advent of Code 2017 - Day 17: Spinlock (Part 1)

Simulate a spinlock algorithm that builds a circular buffer:
1. Start with buffer [0] at position 0
2. Step forward by the step size
3. Insert the next value after current position
4. The newly inserted value becomes the current position
5. Repeat for 2017 insertions (inserting values 1-2017)

Find the value immediately after 2017 in the final buffer.

Example with step size 3:
    [0] -> [0, 1] -> [0, 2, 1] -> [0, 2, 3, 1] -> ...
    After 2017 insertions, find the value after 2017 in the buffer.
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/17/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def simulate_spinlock(step_size, num_insertions):
    """
    Simulate the spinlock algorithm.

    Args:
        step_size: Number of steps to move forward each iteration
        num_insertions: Number of values to insert (1 through num_insertions)

    Returns:
        Tuple of (circular_buffer, final_position)
    """
    buffer = [0]
    current_position = 0

    for value in range(1, num_insertions + 1):
        # Step forward
        current_position = (current_position + step_size) % len(buffer)

        # Insert new value after current position
        buffer.insert(current_position + 1, value)

        # Move to newly inserted position
        current_position += 1

    return buffer, current_position


def main():
    """Simulate spinlock and find value after 2017."""
    step_size = 328
    num_insertions = 2017

    buffer, final_position = simulate_spinlock(step_size, num_insertions)

    # Find value after 2017 in the buffer
    idx_2017 = buffer.index(2017)
    value_after_2017 = buffer[idx_2017 + 1]

    AoCUtils.print_solution(1, value_after_2017)


if __name__ == "__main__":
    main()
