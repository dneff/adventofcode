"""
Advent of Code 2018 - Day 22: Mode Maze (Part 1)
https://adventofcode.com/2018/day/22

Determine the risk level of the area in the cave system by calculating the sum of
the risk levels of all regions within the rectangle defined by the mouth of the cave
(at 0,0) and the target coordinates.

The cave system consists of regions at integer coordinates, each with:
- Geologic Index: Calculated based on position
- Erosion Level: (geologic index + depth) % 20183
- Region Type: erosion level % 3 (0=rocky, 1=wet, 2=narrow)
- Risk Level: Same as region type (0, 1, or 2)
"""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, "../../../../aoc-data/2018/22/input")
sys.path.append(os.path.join(SCRIPT_DIR, "../../"))

from aoc_helpers import AoCInput, AoCUtils

# Parse input: cave depth and target coordinates
input_lines = AoCInput.read_lines(INPUT_FILE)
cave_depth = int(input_lines[0].split(": ")[1])
target_x, target_y = map(int, input_lines[1].split(": ")[1].split(","))
target_coords = (target_x, target_y)


def calculate_erosion_level(erosion_cache, x, y):
    """
    Calculate the erosion level for a cave region at coordinates (x, y).

    Erosion level calculation:
    1. Determine geologic index based on position:
       - Origin (0,0) and target: geologic index = 0
       - Y=0 (top edge): geologic index = X * 16807
       - X=0 (left edge): geologic index = Y * 48271
       - Other regions: geologic index = erosion_left * erosion_above
    2. Erosion level = (geologic index + cave_depth) % 20183

    Args:
        erosion_cache: Dictionary caching previously calculated erosion levels
        x, y: Coordinates of the region

    Returns:
        int: The erosion level for the region at (x, y)
    """
    # Return cached value if already calculated
    if (x, y) in erosion_cache:
        return erosion_cache[(x, y)]

    # Calculate geologic index based on position
    if (x, y) == (0, 0) or (x, y) == target_coords:
        # Mouth of cave and target have geologic index 0
        geologic_index = 0
    elif y == 0:
        # Top edge: geologic index = X * 16807
        geologic_index = x * 16807
    elif x == 0:
        # Left edge: geologic index = Y * 48271
        geologic_index = y * 48271
    else:
        # Interior regions: geologic index = erosion_left * erosion_above
        erosion_left = calculate_erosion_level(erosion_cache, x - 1, y)
        erosion_above = calculate_erosion_level(erosion_cache, x, y - 1)
        geologic_index = erosion_left * erosion_above

    # Calculate erosion level from geologic index
    erosion_level = (geologic_index + cave_depth) % 20183

    # Cache the result
    erosion_cache[(x, y)] = erosion_level

    return erosion_level

# Cache for erosion levels to avoid recalculation
erosion_cache = {}

# Calculate risk level for each region in the rectangle from (0,0) to target
# Risk level = erosion level % 3 (gives region type: 0=rocky, 1=wet, 2=narrow)
total_risk_level = 0

for y in range(0, target_y + 1):
    for x in range(0, target_x + 1):
        erosion_level = calculate_erosion_level(erosion_cache, x, y)
        region_type = erosion_level % 3  # 0=rocky, 1=wet, 2=narrow
        total_risk_level += region_type

AoCUtils.print_solution(1, total_risk_level)