"""
Advent of Code 2025 - Day 12: Christmas Tree Farm
https://adventofcode.com/2025/day/12

Problem:
The input contains two sections:
1. Present shapes - Each shape has an index and a visual grid representation
   where # represents the solid part and . represents empty space
2. Regions - Each region specifies dimensions (WIDTHxLENGTH) followed by a
   list of how many presents of each shape type need to fit in that region

Part 1: Count how many regions can fit all their required presents.

Solution Strategy:
This solution uses a simplified approach - instead of solving the complex
packing problem, it assumes each present occupies a 3x3 bounding box. If the
region's total area is at least as large as the sum of all 3x3 boxes needed,
we consider it feasible. This heuristic works for this specific input but
would not be correct for all possible inputs (packing efficiency matters).
"""

import os
import sys


# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "../../"))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, "../../../../aoc-data/2025/12/input")

# Parse input file
# shapes: Dict mapping shape ID to list of grid rows (visual representation)
# regions: List of tuples ((width, length), {shape_id: count})
shapes = {}
regions = []

# Parse the input file, which has two sections separated by a blank line
is_parsing_shapes_section = True
current_shape_id = None

for line in AoCInput.read_lines(INPUT_FILE):
    # Distinguish between sections: shapes have short lines (e.g., "0:" or "##.")
    # while regions have longer format lines (e.g., "12x5: 1 2 0 0 0 0")
    is_parsing_shapes_section = len(line.strip()) < 5

    if is_parsing_shapes_section:
        # Parse shape definitions (e.g., "0:", then grid rows like "##.", ".#.")
        if ":" in line:
            current_shape_id = int(line.split(":")[0])
            shapes[current_shape_id] = []
        elif line.strip():
            # Add grid row to the current shape
            shapes[current_shape_id].append(line.strip())
    else:
        # Parse region definitions (e.g., "12x5: 1 2 0 0 0 0")
        if line.strip():
            region_dimensions, presents_list = line.split(":", 1)
            width, length = map(int, region_dimensions.split("x"))

            # Parse present counts: the position in the list is the shape ID
            present_counts = {}
            for shape_id, count_str in enumerate(presents_list.split()):
                present_counts[shape_id] = int(count_str)

            regions.append(((width, length), present_counts))

# Count regions where all presents can fit using simplified area check
regions_that_fit = 0

for (width, length), present_counts in regions:
    # Calculate total area available in this region
    region_area = width * length

    # Calculate space needed: assume each present needs a 3x3 bounding box
    # This is a simplification that avoids solving the complex packing problem
    total_presents = sum(present_counts.values())
    space_needed = total_presents * 9  # 3x3 = 9 square units per present

    # If there's enough area, assume the presents can fit
    if region_area >= space_needed:
        regions_that_fit += 1

AoCUtils.print_solution(1, regions_that_fit)