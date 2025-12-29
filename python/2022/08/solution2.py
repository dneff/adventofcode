"""
Advent of Code 2022 - Day 8, Part 2
https://adventofcode.com/2022/day/8

This script finds the highest scenic score for any tree.
"""

import os
import sys
from math import prod

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2022/8/input')


def score_position(height, trees):
    """
    Calculate the viewing distance score in one direction.

    Args:
        height: Height of the tree
        trees: List of trees in viewing direction

    Returns:
        int: Number of trees visible
    """
    distance = 0
    for tree in trees:
        distance += 1
        if tree >= height:
            break
    return max(distance, 1)


def solve_part2():
    """
    Find the highest scenic score possible for any tree.

    Returns:
        int: Highest scenic score
    """
    lines = AoCInput.read_lines(INPUT_FILE)
    forest = []
    for line in lines:
        trees = [int(x) for x in line]
        forest.append(trees)

    edge_min = 0
    edge_max = len(forest) - 1

    best_score = 0

    for y, trees in enumerate(forest):
        for x, tree in enumerate(trees):
            # Skip edge trees (score would be 0)
            if edge_min in [x, y] or edge_max in [x, y]:
                continue

            # Get trees in each direction
            left_trees = [forest[y][z] for z in range(edge_min, x)]
            right_trees = [forest[y][z] for z in range(x + 1, edge_max + 1)]
            up_trees = [forest[z][x] for z in range(edge_min, y)]
            down_trees = [forest[z][x] for z in range(y + 1, edge_max + 1)]

            # Reverse left and up to orient from tree's perspective
            left_trees = left_trees[::-1]
            up_trees = up_trees[::-1]

            # Calculate scenic score
            visibility = []
            for direction_trees in [left_trees, right_trees, up_trees, down_trees]:
                visibility.append(score_position(forest[y][x], direction_trees))
            best_score = max(best_score, prod(visibility))

    return best_score


# Compute and print the answer for part 2
answer = solve_part2()
AoCUtils.print_solution(2, answer)
