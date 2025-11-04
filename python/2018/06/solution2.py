"""
Advent of Code 2018 - Day 6: Chronal Coordinates (Part 2)
https://adventofcode.com/2018/day/6

Find the size of the region containing all locations which have a total Manhattan
distance to all given coordinates of less than 10000.

This creates a safe region where you're not too far from any of the coordinates.
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2018/6/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils, MathUtils


def is_in_safe_region(point, coordinates, max_total_distance=10000):
    """
    Check if a point is in the safe region (total distance to all coords < threshold).

    Args:
        point: (x, y) tuple
        coordinates: List of (x, y) coordinate tuples
        max_total_distance: Maximum allowed total distance

    Returns:
        bool: True if point is in the safe region
    """
    total_distance = sum(MathUtils.manhattan_distance(point, coord)
                        for coord in coordinates)
    return total_distance < max_total_distance


def solve_part2():
    """
    Find the size of the safe region with total distance to all coordinates < 10000.

    Returns:
        int: Number of locations in the safe region
    """
    lines = AoCInput.read_lines(INPUT_FILE)
    coordinates = []

    for line in lines:
        x, y = line.strip().split(', ')
        coordinates.append((int(x), int(y)))

    # Find bounding box
    x_coords = [x for x, y in coordinates]
    y_coords = [y for x, y in coordinates]
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)

    # Count points in the safe region
    safe_region_size = 0

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if is_in_safe_region((x, y), coordinates):
                safe_region_size += 1

    return safe_region_size


# Compute and print the answer for part 2
region_size = solve_part2()
AoCUtils.print_solution(2, region_size)
