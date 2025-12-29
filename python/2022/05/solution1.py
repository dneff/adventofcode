"""
Advent of Code 2022 - Day 5: Supply Stacks
https://adventofcode.com/2022/day/5

This script simulates moving crates one at a time between stacks.
"""

import os
import sys
from collections import defaultdict

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2022/5/input')


def move_crates(cargo, count, src, dest):
    """
    Move crates from source to destination stack, one at a time (reversed).

    Args:
        cargo: Dictionary of stacks
        count: Number of crates to move
        src: Source stack number
        dest: Destination stack number
    """
    grab = cargo[src][-count:]
    cargo[src] = cargo[src][:-count]
    # Reverse because we're moving one at a time
    grab = grab[::-1]
    cargo[dest].extend(grab)


def solve_part1():
    """
    Simulate crate movements and return the top crates.

    Returns:
        str: Top crate from each stack
    """
    lines = AoCInput.read_lines(INPUT_FILE)
    cargo = defaultdict(list)

    # Parse initial cargo configuration
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith('1'):
            break
        for pos, c in enumerate(line.rstrip()):
            if c not in [' ', '[', ']']:
                cargo[1 + (pos // 4)].insert(0, c)
        i += 1

    # Skip to instructions (after blank line)
    i += 2
    while i < len(lines):
        instruction = lines[i].split()
        move_crates(cargo, int(instruction[1]), int(instruction[3]), int(instruction[5]))
        i += 1

    # Get top crates
    top_crates = [cargo[x][-1] for x in range(1, len(cargo) + 1)]
    return ''.join(top_crates)


# Compute and print the answer for part 1
answer = solve_part1()
AoCUtils.print_solution(1, answer)
