"""
Advent of Code 2018 - Day 8: Memory Maneuver
https://adventofcode.com/2018/day/8

The navigation system's license file is encoded as a tree structure represented by a sequence
of numbers. Each node consists of a header (number of child nodes and metadata entries),
followed by child nodes, then metadata entries.

Part 2: Calculate the value of the root node using special rules:
- If a node has no children, its value is the sum of its metadata entries
- If a node has children, metadata entries become 1-indexed references to children,
  and the node's value is the sum of the referenced children's values
"""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2018/8/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


class Node:
    """Represents a node in the license file tree."""

    def __init__(self):
        self.children = []
        self.metadata = []

    def get_value(self):
        """
        Calculate the value of this node according to Part 2 rules.

        Returns:
            int: Value of this node
        """
        # If no children, value is sum of metadata
        if not self.children:
            return sum(self.metadata)

        # If has children, metadata are 1-indexed references to children
        value = 0
        for child_index in self.metadata:
            # Metadata is 1-indexed, convert to 0-indexed
            if 1 <= child_index <= len(self.children):
                value += self.children[child_index - 1].get_value()

        return value


def parse_node(numbers):
    """
    Recursively parse a node from the number sequence.

    Args:
        numbers: List of integers representing the tree structure

    Returns:
        Node: The parsed node with all children and metadata
    """
    node = Node()

    # Parse header
    num_children = numbers.pop(0)
    num_metadata = numbers.pop(0)

    # Parse all child nodes
    for _ in range(num_children):
        node.children.append(parse_node(numbers))

    # Parse metadata entries
    for _ in range(num_metadata):
        node.metadata.append(numbers.pop(0))

    return node


def solve_part2():
    """
    Parse the license file and calculate the value of the root node.

    Returns:
        int: Value of the root node
    """
    # Read input as a single line of space-separated integers
    line = AoCInput.read_lines(INPUT_FILE)[0]
    numbers = [int(x) for x in line.split()]

    # Parse the tree structure
    root = parse_node(numbers)

    # Calculate and return the value of the root node
    return root.get_value()


# Compute and print the answer
answer = solve_part2()
AoCUtils.print_solution(2, answer)