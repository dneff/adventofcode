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

Part 2:

The distress beacon is not detected by any sensor, but the
distress beacon must have x and y coordinates each no lower
than 0 and no larger than 4000000.

Find the only possible position for the distress beacon. What
is its tuning frequency?

Its tuning frequency can be found by multiplying its x coordinate
by 4000000 and then adding its y coordinate.

Strategy:
The distress beacon must be just outside the coverage area of the sensors.
For each sensor with range r, the boundary at distance r+1 consists of 4
diagonal lines (slopes +1 and -1). The beacon must be at an intersection
of these boundary lines. We collect all boundary lines from all sensors,
find their intersection points, and check which intersection is not covered
by any sensor. This is much more efficient than checking all 16 trillion
positions in the search space.
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

def calculate_tuning_frequency(x, y):
    """
    Calculate the tuning frequency for a beacon position.

    The tuning frequency is: x * 4000000 + y

    Args:
        x (int): x-coordinate of the beacon
        y (int): y-coordinate of the beacon

    Returns:
        int: The tuning frequency
    """
    return x * 4000000 + y


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

# Part 2: Find the distress beacon within the search space
SEARCH_MIN = 0
SEARCH_MAX = 4000000


def is_covered(x, y):
    """Check if position (x, y) is covered by any sensor."""
    for (sx, sy), sr in sensor_map.items():
        if abs(x - sx) + abs(y - sy) <= sr:
            return True
    return False


# Optimized approach: The beacon is at the intersection of sensor boundary lines.
# A sensor's boundary consists of 4 diagonal lines. We find where these lines intersect
# and check those intersection points.
#
# For a sensor at (sx, sy) with range r, the boundary lines (at distance r+1) are:
#   Positive slope (+1): y = x + (sy - sx - (r+1))  and  y = x + (sy - sx + (r+1))
#   Negative slope (-1): y = -x + (sy + sx - (r+1))  and  y = -x + (sy + sx + (r+1))

positive_lines = set()  # Lines with slope +1: y = x + b
negative_lines = set()  # Lines with slope -1: y = -x + b

for (sx, sy), sr in sensor_map.items():
    d = sr + 1
    # Add the 4 boundary lines for this sensor
    positive_lines.add(sy - sx - d)  # Top-left and bottom-right edges
    positive_lines.add(sy - sx + d)
    negative_lines.add(sy + sx - d)  # Top-right and bottom-left edges
    negative_lines.add(sy + sx + d)

# Find intersections between positive and negative slope lines
for pos_b in positive_lines:
    for neg_b in negative_lines:
        # Intersection of y = x + pos_b and y = -x + neg_b
        # x + pos_b = -x + neg_b
        # 2x = neg_b - pos_b
        # x = (neg_b - pos_b) / 2
        x = (neg_b - pos_b) // 2
        y = x + pos_b

        # Check if intersection is within bounds
        if SEARCH_MIN <= x <= SEARCH_MAX and SEARCH_MIN <= y <= SEARCH_MAX:
            # Check if this position is NOT covered by any sensor
            if not is_covered(x, y):
                # Found the distress beacon!
                tuning_frequency = calculate_tuning_frequency(x, y)
                AoCUtils.print_solution(2, tuning_frequency)
                exit(0)

