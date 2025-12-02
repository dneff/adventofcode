"""
Advent of Code 2025 - Day 1: Secret Entrance
https://adventofcode.com/2025/day/1

The input contains a sequence of rotations, one per line, which tell you how to 
open the safe. A rotation starts with an L or R which indicates whether the rotation 
should be to the left (toward lower numbers) or to the right (toward higher numbers). 
Then, the rotation has a distance value which indicates how many clicks the dial 
should be rotated in that direction.

Part 1
Analyze the rotations in the input. What's the actual password to open the door?

"""

import os
import sys
from itertools import accumulate, islice

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
def apply_rotation(position, rotation):
    direction, distance = rotation[0], int(rotation[1:])
    return (position + direction_map[direction] * distance) % DIAL_POSITIONS
positions = accumulate(rotation_steps, apply_rotation, initial=STARTING_POSITION)
zero_alignment_count = sum(pos == 0 for pos in islice(positions, 1, None))

AoCUtils.print_solution(1, zero_alignment_count)
