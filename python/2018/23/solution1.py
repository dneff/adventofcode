"""
Advent of Code 2018 - Day 23: Experimental Emergency Teleportation (Part 1)
https://adventofcode.com/2018/day/23

Part 1:
Find the nanobot with the largest signal radius. How many nanobots are in range of its signals?
"""

from collections import defaultdict
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, "../../../../aoc-data/2018/23/input")
sys.path.append(os.path.join(SCRIPT_DIR, "../../"))

from aoc_helpers import AoCInput, AoCUtils


def manhattan_distance_3d(point1, point2):
    """
    Calculate Manhattan distance between two 3D points.

    Manhattan distance is the sum of absolute differences in each dimension.
    For example: distance from (0,0,0) to (1,2,3) = |1-0| + |2-0| + |3-0| = 6

    Args:
        point1: Tuple of (x, y, z) coordinates
        point2: Tuple of (x, y, z) coordinates

    Returns:
        Integer distance between the two points
    """
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1]) + abs(point1[2] - point2[2])


def parse_input(input_lines):
    """
    Parse nanobot data from input lines.

    Each line format: "pos=<x,y,z>, r=radius"
    Example: "pos=<0,0,0>, r=4"

    Args:
        input_lines: List of strings from input file

    Returns:
        List of tuples: ((x, y, z), signal_radius)
    """
    nanobots = []
    for line in input_lines:
        line = line.strip()
        # Split into position part "pos=<x,y,z>" and radius part "radius_value"
        position_part, radius_part = line.split(", r=")

        # Extract x, y, z from "pos=<x,y,z>" by removing "pos=<" prefix and ">" suffix
        x_str, y_str, z_str = position_part[5:-1].split(",")
        x, y, z = int(x_str), int(y_str), int(z_str)
        position = (x, y, z)

        # Parse signal radius
        signal_radius = int(radius_part)

        nanobots.append((position, signal_radius))
    return nanobots


def find_strongest_nanobot(nanobots):
    """
    Find the nanobot with the largest signal radius.

    The "strongest" nanobot is defined as the one that can transmit
    signals the farthest distance.

    Args:
        nanobots: List of tuples ((x, y, z), signal_radius)

    Returns:
        Tuple: ((x, y, z), signal_radius) of the strongest nanobot
    """
    strongest_nanobot = None
    max_signal_radius = 0

    for nanobot in nanobots:
        position, signal_radius = nanobot
        if signal_radius > max_signal_radius:
            max_signal_radius = signal_radius
            strongest_nanobot = nanobot

    return strongest_nanobot


def create_bot_map(nanobots):
    """
    Create a mapping of each nanobot position to all nanobots within its range.

    For each nanobot, determine which other nanobots (including itself) are
    within signal range based on Manhattan distance.

    Args:
        nanobots: List of tuples ((x, y, z), signal_radius)

    Returns:
        Dictionary mapping position tuples to sets of nanobots in range:
        {(x, y, z): {nanobot1, nanobot2, ...}}
    """
    bot_range_map = defaultdict(set)

    # Compare each pair of nanobots to see if they're in range of each other
    for source_bot in nanobots:
        source_position, source_radius = source_bot
        for target_bot in nanobots:
            target_position, target_radius = target_bot

            # Calculate distance between the two nanobots
            distance = manhattan_distance_3d(source_position, target_position)

            # Check if target_bot is within source_bot's signal range
            if distance <= source_radius:
                bot_range_map[source_position].add(target_bot)

            # Check if source_bot is within target_bot's signal range
            if distance <= target_radius:
                bot_range_map[target_position].add(source_bot)

    return bot_range_map

def main():
    """
    Solve Part 1: Find how many nanobots are in range of the strongest nanobot.

    Strategy:
    1. Parse all nanobots from input
    2. Create a map of which nanobots are in range of each nanobot
    3. Find the nanobot with the largest signal radius (strongest)
    4. Count how many nanobots are within the strongest nanobot's range
    """
    # Read and parse input file
    input_lines = AoCInput.read_lines(INPUT_FILE)
    nanobots = parse_input(input_lines)

    # Build a map of which bots are in range of each bot
    bot_range_map = create_bot_map(nanobots)

    # Find the nanobot with the largest signal radius
    strongest_nanobot = find_strongest_nanobot(nanobots)
    strongest_position = strongest_nanobot[0]

    # Count how many nanobots are within range of the strongest nanobot
    # (including the strongest nanobot itself)
    nanobots_in_range_of_strongest = len(bot_range_map[strongest_position])

    AoCUtils.print_solution(1, nanobots_in_range_of_strongest)

if __name__ == "__main__":
    main()
