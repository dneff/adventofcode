"""
Advent of Code 2019 - Day 10: Monitoring Station - Part 2

Once the monitoring station is placed, a giant rotating laser vaporizes asteroids
starting from pointing up (0 degrees) and rotating clockwise. The laser only
vaporizes one asteroid per angle per rotation. Find the 200th asteroid to be
vaporized and calculate its coordinate checksum (x*100 + y).
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


def find_best_monitoring_station(asteroids):
    """
    Find the asteroid position that can see the most other asteroids.

    Args:
        asteroids: List of all asteroid positions

    Returns:
        Tuple (best_position, max_visible_count)
    """
    max_visible = 0
    best_location = None

    for base_asteroid in asteroids:
        visible_angles = {}
        for asteroid in asteroids:
            if base_asteroid == asteroid:
                continue
            distance, angle = calculate_angle(base_asteroid, asteroid)
            visible_angles[angle] = asteroid

        visible_count = len(visible_angles)
        if visible_count > max_visible:
            max_visible = visible_count
            best_location = base_asteroid

    return best_location


def find_vaporization_target(station_position, asteroids, target_number):
    """
    Find the Nth asteroid to be vaporized by the rotating laser.

    The laser starts pointing up and rotates clockwise. For each angle,
    it vaporizes the closest asteroid at that angle.

    Args:
        station_position: Position of the monitoring station
        asteroids: List of all asteroid positions
        target_number: Which asteroid to find (200th = index 199)

    Returns:
        Coordinate checksum (x*100 + y) of the target asteroid
    """
    # Map angles to the closest asteroid at each angle
    closest_at_angle = {}

    for asteroid in asteroids:
        if station_position == asteroid:
            continue

        distance, angle = calculate_angle(station_position, asteroid)

        # Keep only the closest asteroid at each angle (first to be vaporized)
        if angle not in closest_at_angle:
            closest_at_angle[angle] = (asteroid[0], asteroid[1], distance)
        else:
            if distance < closest_at_angle[angle][2]:
                closest_at_angle[angle] = (asteroid[0], asteroid[1], distance)

    # Sort angles to get vaporization order (clockwise from 0)
    vaporization_angles = sorted(closest_at_angle.keys())

    # Get the target asteroid (200th = index 199)
    target_angle = vaporization_angles[target_number - 1]
    target_asteroid = closest_at_angle[target_angle]

    # Return checksum: x*100 + y
    return target_asteroid[0] * 100 + target_asteroid[1]


def solve_part2():
    """Find the 200th asteroid to be vaporized and return its checksum."""
    lines = AoCInput.read_lines(INPUT_FILE)
    asteroids = parse_asteroid_map(lines)

    # First, find the best monitoring station location
    station = find_best_monitoring_station(asteroids)

    # Then find the 200th vaporized asteroid
    return find_vaporization_target(station, asteroids, 200)


answer = solve_part2()
AoCUtils.print_solution(2, answer)
