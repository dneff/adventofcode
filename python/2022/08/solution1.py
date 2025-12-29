"""
Advent of Code 2022 - Day 8: Treetop Tree House
https://adventofcode.com/2022/day/8

This script counts how many trees are visible from outside the grid.
"""

import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2022/8/input')


def solve_part1():
    """
    Count the number of trees visible from outside the grid.

    Returns:
        int: Number of visible trees
    """
    lines = AoCInput.read_lines(INPUT_FILE)
    forest = []
    for line in lines:
        trees = [int(x) for x in line]
        forest.append(trees)

    edge_min = 0
    edge_max = len(forest) - 1

    visible = 0

    for y, trees in enumerate(forest):
        for x, tree in enumerate(trees):
            # Edge trees are always visible
            if edge_min in [x, y] or edge_max in [x, y]:
                visible += 1
            else:
                # Check visibility from each direction
                left_trees = trees[:x]
                right_trees = trees[x + 1:]
                up_trees = [forest[z][x] for z in range(edge_min, y)]
                down_trees = [forest[z][x] for z in range(y + 1, edge_max + 1)]

                if all([t < tree for t in left_trees]) or \
                   all([t < tree for t in right_trees]) or \
                   all([t < tree for t in up_trees]) or \
                   all([t < tree for t in down_trees]):
                    visible += 1

    return visible


# Compute and print the answer for part 1
answer = solve_part1()
AoCUtils.print_solution(1, answer)
