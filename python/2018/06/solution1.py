"""
Advent of Code 2018 - Day 6: Chronal Coordinates (Part 1)
https://adventofcode.com/2018/day/6

Determine the area around each coordinate by counting the number of integer (X,Y)
locations that are closest to that coordinate using Manhattan distance.

Find the largest finite area that isn't infinite. Coordinates with areas extending
to the grid boundary are considered infinite and should be excluded.

Tied locations (equidistant from multiple coordinates) don't count toward any area.
"""

import os
import sys
from collections import defaultdict
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2018/6/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils, MathUtils


def find_closest_coordinate(point, coordinates):
    """
    Find the closest coordinate to a given point using Manhattan distance.

    Args:
        point: (x, y) tuple
        coordinates: List of (x, y) coordinate tuples

    Returns:
        tuple: Closest coordinate, or (-1, -1) if tied between multiple coordinates
    """
    # Calculate distances to all coordinates
    distances = [(coord, MathUtils.manhattan_distance(point, coord))
                 for coord in coordinates]
    distances.sort(key=lambda x: x[1])

    # If there's a tie for closest, return sentinel value
    if distances[0][1] == distances[1][1]:
        return (-1, -1)
    else:
        return distances[0][0]


def solve_part1():
    """
    Find the size of the largest finite area around any coordinate.

    Returns:
        int: Size of the largest finite area
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

    # Find coordinates with infinite areas (extend beyond boundary)
    infinite_coordinates = set()

    # Check points outside the boundary to find infinite areas
    for border_x in range(min_x - 10, max_x + 11):
        infinite_coordinates.add(find_closest_coordinate((border_x, min_y - 10), coordinates))
        infinite_coordinates.add(find_closest_coordinate((border_x, max_y + 10), coordinates))

    for border_y in range(min_y - 10, max_y + 11):
        infinite_coordinates.add(find_closest_coordinate((min_x - 10, border_y), coordinates))
        infinite_coordinates.add(find_closest_coordinate((max_x + 10, border_y), coordinates))

    # Calculate areas for each coordinate
    areas = defaultdict(int)

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            closest = find_closest_coordinate((x, y), coordinates)
            if closest not in infinite_coordinates:
                areas[closest] += 1

    # Return the largest finite area
    return max(areas.values())


# Compute and print the answer for part 1
largest_area = solve_part1()
AoCUtils.print_solution(1, largest_area)
