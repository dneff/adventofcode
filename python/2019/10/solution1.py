"""
Advent of Code 2019 - Day 10: Monitoring Station - Part 1

Find the best asteroid location for a monitoring station. The best location
is the asteroid from which the most other asteroids can be detected. An asteroid
can detect another if there's a direct line of sight (no other asteroid blocks
the view on the same angle).
"""
import os
import sys
import math

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/10/input')


def calculate_angle(base_position, asteroid_position):
    """
    Calculate the angle from base to asteroid.

    The angle is adjusted so that 0 degrees points up (north) and
    angles increase clockwise.

    Args:
        base_position: Tuple (x, y) of base asteroid
        asteroid_position: Tuple (x, y) of target asteroid

    Returns:
        Tuple of (distance, angle_in_degrees)
    """
    delta_x = asteroid_position[0] - base_position[0]
    delta_y = asteroid_position[1] - base_position[1]

    distance = (delta_x ** 2 + delta_y ** 2) ** 0.5
    # Adjust angle: add 90 to rotate coordinate system so 0 degrees points up
    angle = (math.degrees(math.atan2(delta_y, delta_x)) + 90) % 360

    return round(distance, 3), round(angle, 3)


def parse_asteroid_map(lines):
    """
    Parse asteroid map into list of asteroid coordinates.

    Args:
        lines: Grid of characters where '#' represents an asteroid

    Returns:
        List of (x, y) tuples representing asteroid positions
    """
    asteroids = []
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == '#':
                asteroids.append((col, row))
    return asteroids


def count_visible_asteroids(base_asteroid, all_asteroids):
    """
    Count how many asteroids are visible from the base position.

    An asteroid is visible if no other asteroid blocks the line of sight
    (i.e., has the same angle but closer distance).

    Args:
        base_asteroid: Position to check from
        all_asteroids: List of all asteroid positions

    Returns:
        Number of visible asteroids from base position
    """
    visible_angles = {}

    for asteroid in all_asteroids:
        if base_asteroid == asteroid:
            continue

        distance, angle = calculate_angle(base_asteroid, asteroid)
        # Only keep one asteroid per angle (the first one encountered blocks others)
        visible_angles[angle] = asteroid

    return len(visible_angles)


def solve_part1():
    """Find the asteroid with the best monitoring station location."""
    lines = AoCInput.read_lines(INPUT_FILE)
    asteroids = parse_asteroid_map(lines)

    max_visible = 0
    best_location = None

    for asteroid in asteroids:
        visible_count = count_visible_asteroids(asteroid, asteroids)
        if visible_count > max_visible:
            max_visible = visible_count
            best_location = asteroid

    return max_visible


answer = solve_part1()
AoCUtils.print_solution(1, answer)
