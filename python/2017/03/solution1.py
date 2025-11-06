"""
Advent of Code 2017 - Day 3: Spiral Memory (Part 1)

Calculate the Manhattan distance from a given square number to square 1 (the center) in a
spiral memory allocation pattern. Data is arranged in a square spiral starting from 1 at the
center and spiraling outward.

Examples:
    - Square 1: 0 steps (already at the center)
    - Square 12: 3 steps
    - Square 23: 2 steps
    - Square 1024: 31 steps
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/3/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCUtils  # noqa: E402


def build_spiral_to_target(target_square):
    """
    Build a spiral memory pattern up to the target square number.

    Args:
        target_square: The square number we need to reach

    Returns:
        Tuple of (x, y) coordinates of the target square
    """
    # Directions: Right, Up, Left, Down
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    current_dir = 0
    x, y = 0, 0
    square_number = 1
    visited_squares = {}

    # Place square 1 at the center
    visited_squares[(x, y)] = square_number
    square_number += 1

    # Move right to start the spiral
    x, y = x + directions[current_dir][0], y + directions[current_dir][1]
    visited_squares[(x, y)] = square_number
    current_dir += 1

    # Continue spiraling until we reach the target
    while square_number <= target_square:
        square_number += 1

        # Check if we should turn (if the left position is unvisited)
        next_dir = (current_dir + 1) % 4
        next_loc = (x + directions[next_dir][0], y + directions[next_dir][1])
        if next_loc not in visited_squares:
            current_dir = next_dir

        # Move in the current direction
        next_loc = (x + directions[current_dir][0], y + directions[current_dir][1])
        x, y = next_loc
        visited_squares[next_loc] = square_number

    return x, y


def main():
    """Calculate the Manhattan distance from the target square to square 1."""
    target_square = 347991

    x, y = build_spiral_to_target(target_square)

    # Calculate Manhattan distance (subtract 1 for moves, not locations)
    manhattan_distance = abs(x) + abs(y) - 1
    AoCUtils.print_solution(1, manhattan_distance)


if __name__ == "__main__":
    main()
