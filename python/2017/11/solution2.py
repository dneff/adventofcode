"""
Advent of Code 2017 - Day 11: Hex Ed (Part 2)

Track the furthest distance from the origin during the entire path traversal. Instead
of just calculating the final position's distance, find the maximum distance reached
at any point during the journey.

This requires calculating the hex distance after each move and keeping track of the
maximum value seen throughout all moves.
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/11/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402


class HexGrid():
    """Navigate a hexagonal grid using cube coordinates."""

    # Cube coordinate deltas for each hex direction
    directions = {
        'n':  (0, -1, 1),
        'ne': (1, -1, 0),
        'se': (1, 0, -1),
        's':  (0, 1, -1),
        'sw': (-1, 1, 0),
        'nw': (-1, 0, 1)
    }

    def __init__(self):
        """Initialize at origin (0, 0, 0)."""
        self.position = (0, 0, 0)

    def move(self, direction):
        """
        Move one step in the given direction.

        Args:
            direction: One of 'n', 'ne', 'se', 's', 'sw', 'nw'
        """
        delta = self.directions[direction]
        self.position = (
            self.position[0] + delta[0],
            self.position[1] + delta[1],
            self.position[2] + delta[2]
        )

    def distance(self):
        """
        Calculate hex distance from origin using cube coordinates.

        Returns:
            Number of hex steps from origin to current position
        """
        # Distance is sum of absolute coordinate values divided by 2
        return sum(abs(coord) for coord in self.position) // 2


def main():
    """Follow path and find the maximum distance ever reached."""
    line = AoCInput.read_lines(INPUT_FILE)[0]
    grid = HexGrid()
    moves = line.strip().split(',')
    max_distance = 0

    for move in moves:
        grid.move(move)
        current_distance = grid.distance()
        max_distance = max(max_distance, current_distance)

    AoCUtils.print_solution(2, max_distance)


if __name__ == "__main__":
    main()
