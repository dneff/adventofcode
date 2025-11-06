"""
Advent of Code 2017 - Day 13: Packet Scanners (Part 1)

Navigate through a firewall with security scanners. Each layer has a scanner that moves
up and down continuously. Calculate the total severity of being caught by scanners.

Scanners start at position 0 and move down to (range-1), then back up to 0, repeating
this pattern. They complete a full cycle every (range-1)*2 picoseconds. The packet moves
through one layer per picosecond, starting at time 0.

Severity = depth * range for each layer where you're caught
Total severity = sum of all individual severities

Key insight: A scanner is at position 0 (catching you) when time % ((range-1)*2) == 0

Example:
    0: 3   # Layer 0, range 3, scanner cycles every 4 picoseconds
    1: 2   # Layer 1, range 2, scanner cycles every 2 picoseconds
    4: 4   # Layer 4, range 4, scanner cycles every 6 picoseconds
    6: 4   # Layer 6, range 4, scanner cycles every 6 picoseconds

    Caught at layers 0 and 6, severity = 0*3 + 6*4 = 24
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/13/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402


def parse_firewall(lines):
    """
    Parse firewall layer definitions.

    Args:
        lines: List of strings in format "depth: range"

    Returns:
        Dictionary mapping layer depth to scanner range
    """
    firewall = {}
    for line in lines:
        depth, scanner_range = [int(x) for x in line.split(': ')]
        firewall[depth] = scanner_range
    return firewall


def calculate_trip_severity(firewall):
    """
    Calculate total severity of packet trip through firewall.

    Args:
        firewall: Dictionary mapping depth to range

    Returns:
        Total severity (sum of depth * range for caught layers)
    """
    total_severity = 0

    # Check each layer from 0 to max depth
    for time in range(max(firewall.keys()) + 1):
        if time in firewall:
            scanner_range = firewall[time]
            cycle_length = (scanner_range - 1) * 2

            # Check if scanner is at position 0 when packet arrives
            if time % cycle_length == 0:
                severity = firewall[time] * time
                total_severity += severity

    return total_severity


def main():
    """Calculate and print the trip severity."""
    lines = AoCInput.read_lines(INPUT_FILE)
    firewall = parse_firewall(lines)
    severity = calculate_trip_severity(firewall)
    AoCUtils.print_solution(1, severity)


if __name__ == "__main__":
    main()
