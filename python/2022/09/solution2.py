"""
Advent of Code 2022 - Day 9, Part 2
https://adventofcode.com/2022/day/9

This script simulates a rope with 10 knots tracking positions visited by the tail.
"""

import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2022/9/input')

DIRECTION = {
    "U": (0, 1),
    "R": (1, 0),
    "D": (0, -1),
    "L": (-1, 0),
}


def update_position(position, heading):
    """
    Update the position based on the heading direction.

    Args:
        position: Current position (x, y)
        heading: Direction to move (U/R/D/L)

    Returns:
        tuple: New position
    """
    delta = DIRECTION[heading]
    return (position[0] + delta[0], position[1] + delta[1])


def is_adjacent(head, tail):
    """
    Check if two positions are adjacent (touching).

    Args:
        head: Head position
        tail: Tail position

    Returns:
        bool: True if positions are adjacent
    """
    offset = (abs(head[0] - tail[0]), abs(head[1] - tail[1]))
    return max(offset) < 2


def update_tail(head, tail):
    """
    Move tail one step closer to head.

    Args:
        head: Head position
        tail: Tail position

    Returns:
        tuple: New tail position
    """
    if head[0] > tail[0]:
        tail = (tail[0] + 1, tail[1])
    elif head[0] < tail[0]:
        tail = (tail[0] - 1, tail[1])

    if head[1] > tail[1]:
        tail = (tail[0], tail[1] + 1)
    elif head[1] < tail[1]:
        tail = (tail[0], tail[1] - 1)

    return tail


def solve_part2():
    """
    Simulate 10-knot rope movement and count unique positions visited by tail.

    Returns:
        int: Number of unique positions visited by tail
    """
    lines = AoCInput.read_lines(INPUT_FILE)
    rope = [(0, 0)] * 10
    t_moves = [rope[-1]]

    for line in lines:
        heading, count = line.split()
        count = int(count)

        for _ in range(count):
            for idx, pos in enumerate(rope):
                if idx == 0:
                    rope[idx] = update_position(pos, heading)
                else:
                    if not is_adjacent(pos, rope[idx - 1]):
                        rope[idx] = update_tail(rope[idx - 1], pos)

            t_moves.append(rope[-1])

    return len(set(t_moves))


# Compute and print the answer for part 2
answer = solve_part2()
AoCUtils.print_solution(2, answer)
