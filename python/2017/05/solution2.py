"""
Advent of Code 2017 - Day 5: A Maze of Twisty Trampolines, All Alike (Part 2)

Navigate a maze of jump instructions with a modified rule: after each jump, if the offset was
three or more, decrease it by 1. Otherwise, increase it by 1. Count how many steps it takes to
reach an instruction outside the list.

Example:
    Starting with [0, 3, 0, 1, -3]:
    - The modified rules make escaping take 10 steps instead of 5
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/5/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402


def count_steps_to_exit_with_decrease(jump_offsets):
    """
    Count steps needed to exit with the modified rule for large offsets.

    Args:
        jump_offsets: List of jump offset instructions

    Returns:
        Number of steps to exit the instruction list
    """
    steps = 0
    position = 0

    while 0 <= position < len(jump_offsets):
        steps += 1
        jump_value = jump_offsets[position]

        # Modified rule: decrease if >= 3, otherwise increase
        if jump_value >= 3:
            jump_offsets[position] -= 1
        else:
            jump_offsets[position] += 1

        position += jump_value

    return steps


def main():
    """Calculate steps needed to escape with modified jump rules."""
    lines = AoCInput.read_lines(INPUT_FILE)
    jump_offsets = [int(value) for value in lines]

    steps = count_steps_to_exit_with_decrease(jump_offsets)
    AoCUtils.print_solution(2, steps)


if __name__ == "__main__":
    main()
