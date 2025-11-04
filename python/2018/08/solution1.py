"""
Advent of Code 2018 - Day 8: Memory Maneuver
https://adventofcode.com/2018/day/8

The navigation system's license file is encoded as a tree structure represented by a sequence
of numbers. Each node consists of a header (number of child nodes and metadata entries),
followed by child nodes, then metadata entries.

Part 1: Calculate the sum of all metadata entries in the tree.
"""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2018/8/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def calculate_metadata_sum(numbers):
    """
    Recursively parse the tree structure and sum all metadata entries.

    The tree is defined by consuming numbers from the list:
    - First two numbers are header: [num_children, num_metadata]
    - Next come all child nodes (recursively)
    - Finally come metadata entries

    Args:
        numbers: List of integers representing the tree structure

    Returns:
        int: Sum of all metadata entries in this node and its children
    """
    total_sum = 0

    # Parse header
    num_children = numbers.pop(0)
    num_metadata = numbers.pop(0)

    # Process all child nodes
    for _ in range(num_children):
        total_sum += calculate_metadata_sum(numbers)

    # Add metadata entries
    for _ in range(num_metadata):
        total_sum += numbers.pop(0)

    return total_sum


def solve_part1():
    """
    Parse the license file and calculate the sum of all metadata entries.

    Returns:
        int: Sum of all metadata entries in the tree
    """
    # Read input as a single line of space-separated integers
    line = AoCInput.read_lines(INPUT_FILE)[0]
    numbers = [int(x) for x in line.split()]

    return calculate_metadata_sum(numbers)


# Compute and print the answer
answer = solve_part1()
AoCUtils.print_solution(1, answer)