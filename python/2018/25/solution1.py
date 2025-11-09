"""
Advent of Code 2018 - Day 25: Four Dimensional Adventure
https://adventofcode.com/2018/day/25

The list of fixed points in spacetime (your puzzle input) is a set of four-dimensional 
coordinates. To align your device, acquire the hot chocolate, and save the reindeer, 
you just need to find the number of constellations of points in the list.

How many constellations are formed by the fixed points in spacetime?
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2018/25/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def manhattan_distance(point1, point2):
    """
    Calculate the Manhattan distance between two 4D points in spacetime.

    Two points belong to the same constellation if their Manhattan distance is <= 3.

    Args:
        point1 (tuple): The first point as a tuple of four integers (x, y, z, w)
        point2 (tuple): The second point as a tuple of four integers (x, y, z, w)

    Returns:
        int: The Manhattan distance between the two points
    """
    return sum(abs(a - b) for a, b in zip(point1, point2))


# Parse all fixed points in 4D spacetime from the input file
# Each line contains four comma-separated coordinates: x,y,z,w
fixed_points = []

for line in AoCInput.read_lines(INPUT_FILE):
    fixed_points.append(tuple(map(int, line.strip().split(','))))

# List to hold all discovered constellations
# Each constellation is a list of points that are connected by distance <= 3
constellations = []

# Start building the first constellation with the first point
current_constellation = [fixed_points.pop(0)]
points_checked_without_match = 0

# Continue until all points have been assigned to constellations
while fixed_points:
    # Take the next point to evaluate
    point = fixed_points.pop(0)

    # Check if this point belongs to the current constellation
    # A point belongs if it's within distance 3 of ANY member of the constellation
    for constellation_member in current_constellation:
        if manhattan_distance(point, constellation_member) <= 3:
            # Point belongs to current constellation
            current_constellation.append(point)
            points_checked_without_match = 0
            break
    else:
        # Point doesn't belong to current constellation yet
        # Add it back to the end of the queue for later re-evaluation
        fixed_points.append(point)
        points_checked_without_match += 1

    # If we've checked all remaining points without finding any matches,
    # the current constellation is complete - start a new one
    if not fixed_points or points_checked_without_match >= len(fixed_points):
        constellations.append(current_constellation)
        if fixed_points:
            # Start a new constellation with the next point
            current_constellation = [fixed_points.pop(0)]
        points_checked_without_match = 0

# Append final constellation if it wasn't already appended
if current_constellation and (not constellations or current_constellation not in constellations):
    constellations.append(current_constellation)

# Compute and print the answer for part 1
AoCUtils.print_solution(1, len(constellations))
