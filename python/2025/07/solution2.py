"""
Advent of Code 2025 - Day 7: Laboratories (Part 2)
https://adventofcode.com/2025/day/7

Simulate a quantum tachyon particle moving downward through a manifold diagram.
Unlike Part 1, a single particle takes BOTH paths at each splitter, creating
a branching timeline (many-worlds interpretation).

Part 2: Count the total number of timelines after the particle completes all
possible journeys through the manifold.

"""

import os
import sys
from collections import defaultdict

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

# Parse the diagram to locate the particle start position ('S') and all splitters ('^')
for y, row in enumerate(diagram):
    for x, cell in enumerate(row):
        if cell == "S":
            start_position = (x, y)
        elif cell == "^":
            splitter_positions.add((x, y))

# Track particle positions and the number of timelines at each position
# In quantum mechanics, the particle exists in superposition at multiple positions
position_timeline_counts = defaultdict(int)
position_timeline_counts[start_position] = 1  # Start with one timeline

# Simulate particle movement through the manifold
# Process one vertical level at a time
current_y = start_position[1]
while current_y <= max_y:
    next_generation_counts = defaultdict(int)

    for (x, y), timeline_count in position_timeline_counts.items():
        next_y = y + 1

        # Check if the particle hits a splitter
        if (x, next_y) in splitter_positions:
            # Quantum split: each timeline branches into two
            # The particle takes both left AND right paths simultaneously
            next_generation_counts[(x - 1, next_y)] += timeline_count  # Left branch
            next_generation_counts[(x + 1, next_y)] += timeline_count  # Right branch
        else:
            # Particle continues downward through empty space
            next_generation_counts[(x, next_y)] += timeline_count

    position_timeline_counts = next_generation_counts
    current_y += 1

# Calculate total number of distinct timelines
# This is the sum of all timeline counts at positions where particles exit the manifold
total_timelines = sum(position_timeline_counts.values())
AoCUtils.print_solution(2, total_timelines)