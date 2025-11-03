"""
Advent of Code 2017 - Day 13: Packet Scanners (Part 2)

Find the minimum delay that allows the packet to pass through the firewall without being
caught by any scanner. For each picosecond of delay, all scanners move one step before
the packet begins its journey.

The solution iterates through delay values, checking if the packet would be caught at
any layer. With delay d, the packet reaches layer L at time (L + d), and we check if
a scanner at that layer is at position 0 at that time.

Key: Scanner at layer L with range R is at position 0 when (L + delay) % ((R-1)*2) == 0
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/13/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


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


def is_caught_with_delay(firewall, delay):
    """
    Check if packet is caught at any layer with given delay.

    Args:
        firewall: Dictionary mapping depth to range
        delay: Number of picoseconds to delay before starting

    Returns:
        True if caught at any layer, False otherwise
    """
    for layer_depth in range(max(firewall.keys()) + 1):
        if layer_depth in firewall:
            scanner_range = firewall[layer_depth]
            cycle_length = (scanner_range - 1) * 2
            arrival_time = layer_depth + delay

            # Check if scanner is at position 0 when packet arrives
            if arrival_time % cycle_length == 0:
                return True

    return False


def find_minimum_delay(firewall):
    """
    Find the minimum delay to pass through firewall uncaught.

    Args:
        firewall: Dictionary mapping depth to range

    Returns:
        Minimum delay in picoseconds
    """
    delay = 0
    while True:
        if not is_caught_with_delay(firewall, delay):
            return delay
        delay += 1


def main():
    """Find and print the minimum safe delay."""
    lines = AoCInput.read_lines(INPUT_FILE)
    firewall = parse_firewall(lines)
    min_delay = find_minimum_delay(firewall)
    AoCUtils.print_solution(2, min_delay)


if __name__ == "__main__":
    main()
