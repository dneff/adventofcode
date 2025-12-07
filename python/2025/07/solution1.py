"""
Advent of Code 2025 - Day 7: Laboratories (Part 1)
https://adventofcode.com/2025/day/7

Simulate a tachyon beam moving downward through a manifold diagram.
The beam splits when it encounters a splitter (^), creating two new beams
that continue from the left and right positions of the splitter.

Part 1: Count how many times the beam splits as it travels through the manifold.

"""

import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "../../"))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, "../../../../aoc-data/2025/7/input")
diagram = AoCInput.read_lines(INPUT_FILE)

start_position = ()
splitter_positions = set()
max_y = len(diagram) - 1

# Parse the diagram to locate the beam start position ('S') and all splitters ('^')
for y, row in enumerate(diagram):
    for x, cell in enumerate(row):
        if cell == "S":
            start_position = (x, y)
        elif cell == "^":
            splitter_positions.add((x, y))

active_beams = {start_position}
split_count = 0

# Simulate beam movement through the manifold
# Beams move downward (increasing y) one row at a time
while active_beams:
    next_generation_beams = set()

    for x, y in active_beams:
        next_y = y + 1

        # Skip beams that have exited the bottom of the manifold
        if next_y > max_y:
            continue

        # Check if the beam hits a splitter
        if (x, next_y) in splitter_positions:
            # Beam splits: count the split and create two new beams
            split_count += 1
            next_generation_beams.add((x - 1, next_y))  # Left beam
            next_generation_beams.add((x + 1, next_y))  # Right beam
        else:
            # Beam continues downward through empty space
            next_generation_beams.add((x, next_y))

    active_beams = next_generation_beams

AoCUtils.print_solution(1, split_count)
