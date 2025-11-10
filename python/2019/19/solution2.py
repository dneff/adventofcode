"""
Advent of Code 2019 - Day 19: Tractor Beam - Part 2

Find the closest point to the emitter where a 100x100 square fits entirely
within the tractor beam. The beam expands as it goes farther from the emitter.
Return the answer as X*10000 + Y for the top-left corner of the square.
"""
import os
import sys
import math

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402
from IntCode import IntCode, OutputInterrupt  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/19/input')


def calculate_angle(point):
    """Calculate angle of point from origin."""
    x, y = point
    theta = (math.degrees(math.atan2(y, x)) + 90) % 360
    return round(theta, 3)


def check_point_in_beam(program, point):
    """Check if a point is in the tractor beam."""
    x, y = point
    drone_system = IntCode(program)
    drone_system.push(x)
    drone_system.push(y)

    try:
        drone_system.run()
    except OutputInterrupt:
        result = drone_system.pop()

    return result == 1


def scan_initial_area(program):
    """Scan initial area to determine beam angles."""
    affected = []

    for y in range(50):
        for x in range(50):
            drone_system = IntCode(program)
            drone_system.push(x)
            drone_system.push(y)

            try:
                drone_system.run()
            except OutputInterrupt:
                if drone_system.pop() == 1:
                    affected.append((x, y))

    return affected


def solve_part2():
    """Find closest point where 100x100 square fits in beam."""
    program = AoCInput.read_file(INPUT_FILE).strip()

    # Scan initial area to determine beam edges
    affected = scan_initial_area(program)

    # Calculate beam edge angles
    top_edge = max(affected, key=lambda p: p[0])
    bottom_edge = max(affected, key=lambda p: p[1])
    min_angle = min(calculate_angle(top_edge), calculate_angle(bottom_edge))
    max_angle = max(calculate_angle(top_edge), calculate_angle(bottom_edge))

    # Find starting point where beam is wide enough
    start_y = 200
    while True:
        left_edge = 0
        right_edge = 0
        x = 0

        while right_edge == 0:
            x += 1
            angle = calculate_angle((x, start_y))

            if angle > max_angle:
                continue

            if angle <= max_angle and left_edge == 0:
                left_edge = x
            elif angle < min_angle:
                right_edge = x

        if right_edge - left_edge > 100:
            start_x = right_edge
            break

        start_y += 1

    # Walk along edge to find where 100x100 square fits
    while True:
        if check_point_in_beam(program, (start_x, start_y)):
            start_x += 1
            continue

        start_x -= 1

        # Check if opposite corner of 100x100 square is also in beam
        if check_point_in_beam(program, (start_x - 99, start_y + 99)):
            # Found it! Return encoded coordinates of top-left corner
            result = (start_x - 99) * 10000 + start_y
            break

        start_y += 1

    return result


answer = solve_part2()
AoCUtils.print_solution(2, answer)
