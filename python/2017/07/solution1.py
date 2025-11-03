"""
Advent of Code 2017 - Day 7: Recursive Circus (Part 1)

Find the bottom program in a tower where programs are stacked on top of each other. Each program
has a name, weight, and optionally holds other programs above it. The bottom program is the only
one with no parent (it's not held by any other program).

Example:
    pbga (66)
    xhth (57)
    ebii (61)
    havc (66)
    ktlj (57)
    fwft (72) -> ktlj, cntj, xhth
    qoyq (66)
    padx (45) -> pbga, havc, qoyq
    tknk (41) -> ugml, padx, fwft

    Answer: "tknk" is the bottom program
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/7/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


class ProgramNode():
    """Represents a program in the tower with its relationships."""

    def __init__(self):
        self.name = None
        self.parent = None
        self.score = 0
        self.children = []

    def __getitem__(self, i):
        return self.children[i]


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
        program_nodes[program_name].score = program_weight

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


def find_bottom_program(program_nodes):
    """
    Find the bottom program (the one with no parent).

    Args:
        program_nodes: Dictionary of program name to ProgramNode

    Returns:
        Name of the bottom program
    """
    for program in program_nodes.values():
        if program.parent is None:
            return program.name
    return None


def main():
    """Find and print the name of the bottom program."""
    lines = AoCInput.read_lines(INPUT_FILE)
    program_nodes = parse_programs(lines)
    bottom_program = find_bottom_program(program_nodes)
    AoCUtils.print_solution(1, bottom_program)


if __name__ == "__main__":
    main()
