"""
Advent of Code 2017 - Day 5: A Maze of Twisty Trampolines, All Alike (Part 1)

Navigate a maze of jump instructions where each instruction is a relative offset. After each
jump, the instruction at that position is incremented by 1. Count how many steps it takes to
reach an instruction outside the list.

Example:
    Starting with [0, 3, 0, 1, -3]:
    - Position 0: jump 0 steps (stay), increment to 1
    - Position 0: jump 1 step to position 1, increment to 2
    - Position 1: jump 3 steps to position 4, increment to 4
    - Position 4: jump -3 steps to position 1, increment to -2
    - Position 1: jump 4 steps to position 5 (outside)
    Total: 5 steps
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/5/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402


def count_steps_to_exit(jump_offsets):
    """
    Count steps needed to exit the maze of jump instructions.

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
        jump_offsets[position] += 1
        position += jump_value

    return steps


def main():
    """Calculate steps needed to escape the jump instruction maze."""
    lines = AoCInput.read_lines(INPUT_FILE)
    jump_offsets = [int(value) for value in lines]

    steps = count_steps_to_exit(jump_offsets)
    AoCUtils.print_solution(1, steps)


if __name__ == "__main__":
    main()
