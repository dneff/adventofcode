"""
Advent of Code 2017 - Day 7: Recursive Circus (Part 2)

Find the correct weight for the one unbalanced program in the tower. The tower consists
of programs holding other programs, where each sub-tower should have equal weight. One
program has the wrong weight, causing an imbalance. Determine what that program's weight
should be to balance the entire tower.

The solution uses depth-first traversal to find the unbalanced node - it's the node where
all children are balanced but the parent's children have different total weights.

Example:
    If program 'ugml' and its stack weighs more than its siblings, and ugml needs to be
    8 units lighter for balance, then the answer is ugml's corrected weight.
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/7/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
from collections import defaultdict


class ProgramNode():
    """Represents a program in the tower with weight and parent-child relationships."""

    def __init__(self):
        self.name = None
        self.parent = None
        self.weight = 0
        self.children = []

    def __getitem__(self, i):
        return self.children[i]


def calculate_correct_weight(node):
    """
    Recursively verify balance of each subtree and correct if imbalanced.

    This function traverses the tree depth-first, calculating total weights (node weight
    plus all descendants). When it finds an imbalance (children with different total
    weights), it identifies which child is wrong and calculates the correction needed.

    Args:
        node: ProgramNode to verify and potentially correct

    Returns:
        Total weight of this node and all its descendants
    """
    child_sum = 0
    child_weights = defaultdict(list)

    # Leaf node - just return its weight
    if len(node.children) == 0:
        return node.weight

    # Calculate total weight for each child subtree
    for child in node.children:
        total_child_weight = calculate_correct_weight(child)
        child_weights[total_child_weight].append(child)
        child_sum += total_child_weight

    # Check if children have different total weights (imbalanced)
    if len(set(child_weights.keys())) > 1:
        imbalanced_weight = None
        balanced_weight = None
        imbalanced_node = None

        # Find which child has the wrong weight (appears once vs. multiple times)
        for weight, nodes in child_weights.items():
            if len(nodes) == 1:
                imbalanced_weight = weight
                imbalanced_node = nodes[0]
            else:
                balanced_weight = weight

        # Calculate and apply correction to the problematic node
        correction = balanced_weight - imbalanced_weight
        imbalanced_node.weight += correction
        AoCUtils.print_solution(2, imbalanced_node.weight)

        # Recalculate after correction
        return calculate_correct_weight(node)

    total_weight = child_sum + node.weight
    return total_weight


def parse_programs(lines):
    """
    Parse program definitions and build the tower structure.

    Args:
        lines: List of program definition strings

    Returns:
        Dictionary mapping program names to ProgramNode objects
    """
    program_nodes = {}

    # Create nodes without relationships
    for line in lines:
        program_name, program_weight = line.strip().split()[:2]
        program_weight = int(program_weight.strip('()'))
        program_nodes[program_name] = ProgramNode()
        program_nodes[program_name].name = program_name
        program_nodes[program_name].weight = program_weight

    # Create parent/child relationships
    for line in lines:
        parts = line.strip().split()
        if len(parts) > 3:
            parent_name = parts[0]
            for child_name in parts[3:]:
                child_name = child_name.strip(',')
                program_nodes[parent_name].children.append(program_nodes[child_name])
                program_nodes[child_name].parent = program_nodes[parent_name]

    return program_nodes


def find_root_node(program_nodes):
    """
    Find the root program (the one with no parent).

    Args:
        program_nodes: Dictionary of program name to ProgramNode

    Returns:
        Root ProgramNode
    """
    for program in program_nodes.values():
        if program.parent is None:
            return program
    return None


def main():
    """Find and print the correct weight for the unbalanced program."""
    lines = AoCInput.read_lines(INPUT_FILE)
    program_nodes = parse_programs(lines)
    root = find_root_node(program_nodes)

    # Correct balance if necessary (prints solution internally)
    calculate_correct_weight(root)


if __name__ == "__main__":
    main()
