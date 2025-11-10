"""
Advent of Code 2019 - Day 19: Tractor Beam - Part 1

Use an Intcode program to scan a 50x50 area and determine which points are
affected by a tractor beam. The program takes (x, y) coordinates as input
and outputs 1 if the point is in the beam, 0 otherwise. Count how many
points in the 50x50 grid are affected by the tractor beam.
"""
import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402
from IntCode import IntCode, OutputInterrupt  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/19/input')


def check_point_in_beam(program, x, y):
    """
    Check if a point is affected by the tractor beam.

    Args:
        program: Intcode program string
        x, y: Coordinates to check

    Returns:
        True if point is in beam, False otherwise
    """
    drone_system = IntCode(program)
    drone_system.push(x)
    drone_system.push(y)

    try:
        drone_system.run()
    except OutputInterrupt:
        result = drone_system.pop()

    return result == 1


def solve_part1():
    """Scan 50x50 area and count points affected by tractor beam."""
    program = AoCInput.read_file(INPUT_FILE).strip()

    affected_points = []

    for y in range(50):
        leading_edge = 0
        edge_found = False

        for x in range(50):
            # Optimization: skip to leading edge once found
            if x < leading_edge:
                continue

            drone_system = IntCode(program)
            drone_system.push(x)
            drone_system.push(y)

            try:
                drone_system.run()
            except OutputInterrupt:
                status = drone_system.pop()

                if status == 1:
                    affected_points.append((x, y))
                    if not edge_found:
                        edge_found = True
                        leading_edge = x
                elif status == 0 and edge_found:
                    # Past trailing edge, move to next row
                    break

    return len(affected_points)


answer = solve_part1()
AoCUtils.print_solution(1, answer)
