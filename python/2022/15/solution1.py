"""
Advent of Code 2022 - Day 15: Beacon Exclusion Zone
https://adventofcode.com/2022/day/15

Your pack contains a set of deployable sensors.
Sensors detect the nearest signal source beacon.
Sensors and beacons always exist at integer coordinates.
Each sensor knows its own position and can determine the
position of a beacon precisely; however, sensors can only
lock on to the one beacon closest to the sensor as
measured by the Manhattan distance. (There is never a tie
where two beacons are the same distance to a sensor.)

Because each sensor only identifies its closest beacon, if
a sensor detects a beacon, you know there are no other
beacons that close or closer to that sensor. There could
still be beacons that just happen to not be the closest
beacon to any sensor.

Part 1:

Consult the report from the sensors you just deployed. In the row where
y=2000000, how many positions cannot contain a beacon?

Strategy:
For each sensor, check the distance to the target row. If the distance is less than the sensor's range,
calculate the range of x-coordinates on that row that are within the sensor's range.

Store these ranges and merge them to find the total coverage on the target row.
"""

import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "../../"))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, "../../../../aoc-data/2022/15/input")
sensor_data = AoCInput.read_lines(INPUT_FILE)

def parse_sensor_data(sensor_data):
    """
    Parse sensor and beacon data from input lines.

    Each line contains a sensor position and its closest beacon position.
    Format: "Sensor at x=X, y=Y: closest beacon is at x=X, y=Y"

    Returns:
        sensors (dict): Maps sensor positions (x, y) to their Manhattan distance to closest beacon
        beacons (set): Set of all beacon positions (x, y)
    """
    sensors = {}
    beacons = set()

    for line in sensor_data:
        # Example line: "Sensor at x=2, y=18: closest beacon is at x=-2, y=15"
        parts = line.split()
        sensor_x = int(parts[2][2:-1])  # Extract x from "x=2,"
        sensor_y = int(parts[3][2:-1])  # Extract y from "y=18:"
        beacon_x = int(parts[8][2:-1])  # Extract x from "x=-2,"
        beacon_y = int(parts[9][2:])    # Extract y from "y=15"

        # Calculate Manhattan distance from sensor to its closest beacon
        manhattan_distance = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)

        sensors[(sensor_x, sensor_y)] = manhattan_distance
        beacons.add((beacon_x, beacon_y))

    return sensors, beacons

sensor_map, all_beacons = parse_sensor_data(sensor_data)

# Part 1: Find positions that cannot contain a beacon in row y=2000000
TARGET_ROW_Y = 2000000

# Step 1: Calculate coverage ranges for each sensor on the target row
covered_ranges = set()
for (sensor_x, sensor_y), sensor_range in sensor_map.items():
    # Calculate vertical distance from sensor to target row
    vertical_distance = abs(sensor_y - TARGET_ROW_Y)

    # Check if sensor's range reaches the target row
    if vertical_distance <= sensor_range:
        # Calculate horizontal reach on the target row
        # The sensor covers a diamond shape, so horizontal reach decreases with vertical distance
        horizontal_reach = sensor_range - vertical_distance

        # Add the range of x-coordinates covered by this sensor on the target row
        covered_ranges.add((sensor_x - horizontal_reach, sensor_x + horizontal_reach))

# Step 2: Merge overlapping ranges to avoid double-counting
ranges = sorted(covered_ranges, key=lambda x: x[0])  # Sort by start position
merged = []
for start, end in ranges:
    # If no ranges yet, or current range doesn't overlap with last merged range
    if not merged or merged[-1][1] < start - 1:
        merged.append((start, end))
    else:
        # Ranges overlap or are adjacent, so merge them
        merged[-1] = (merged[-1][0], max(merged[-1][1], end))

# Step 3: Calculate total coverage by summing individual range lengths
total_covered = sum(end - start + 1 for start, end in merged)

# Step 4: Subtract beacons that are actually on the target row
# (these positions CAN contain a beacon, so they shouldn't be counted)
beacons_on_target_row = {beacon_x for (beacon_x, beacon_y) in all_beacons if beacon_y == TARGET_ROW_Y}
total_covered -= len(beacons_on_target_row)

AoCUtils.print_solution(1, total_covered)