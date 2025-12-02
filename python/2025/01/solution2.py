"""
Advent of Code 2025 - Day 1: Secret Entrance
https://adventofcode.com/2025/day/1

The input contains a sequence of rotations, one per line, which tell you how to 
open the safe. A rotation starts with an L or R which indicates whether the rotation 
should be to the left (toward lower numbers) or to the right (toward higher numbers). 
Then, the rotation has a distance value which indicates how many clicks the dial 
should be rotated in that direction.

Part 2

Count the number of times the pointer passes position 0 or is at position 0 while 
following the instructions.
"""

import os
import sys
from collections import deque
from itertools import accumulate

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "../../"))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, "../../../../aoc-data/2025/1/input")
rotation_steps = AoCInput.read_lines(INPUT_FILE)

DIAL_POSITIONS = 100  # Dial positions range from 0 to 99
STARTING_POSITION = 50  # Safe dial starts centered
direction_map = {'L': -1, 'R': 1}
def apply_rotation(state, rotation):
    position, zero_crossings = state
    direction, distance = rotation[0], int(rotation[1:])
    full_turns, remaining = divmod(distance, DIAL_POSITIONS)
    zero_crossings += full_turns
    next_position = (position + direction_map[direction] * remaining) % DIAL_POSITIONS
    if (
        (direction == 'L' and (next_position >= position and position != 0))
        or (direction == 'R' and (next_position <= position and position != 0))
        or next_position == 0
    ):
        zero_crossings += 1
    return next_position, zero_crossings

_, zero_crossings = deque(
    accumulate(rotation_steps, apply_rotation, initial=(STARTING_POSITION, 0)),
    maxlen=1,
)[0]

AoCUtils.print_solution(2, zero_crossings)
