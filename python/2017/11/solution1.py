"""
Advent of Code 2017 - Day 11: Hex Ed (Part 1)

Navigate a hexagonal grid to find a lost child process. The grid uses cube coordinates
(x, y, z) where x + y + z = 0. Calculate the minimum number of steps from the starting
position to the final position after following a path of directional moves.

The hex grid has six directions: n, ne, se, s, sw, nw

Distance calculation: The hex distance is the maximum absolute value of the three
cube coordinates divided by 2 (or equivalently, sum of absolute values / 2).

Examples:
    ne,ne,ne = 3 steps away
    ne,ne,sw,sw = 0 steps away (back at start)
    ne,ne,s,s = 2 steps away (equivalent to se,se)
    se,sw,se,sw,sw = 3 steps away (equivalent to s,s,sw)
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/11/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


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
    """Follow path and calculate final distance from origin."""
    line = AoCInput.read_lines(INPUT_FILE)[0]
    grid = HexGrid()
    moves = line.strip().split(',')

    for move in moves:
        grid.move(move)

    final_distance = grid.distance()
    AoCUtils.print_solution(1, final_distance)


if __name__ == "__main__":
    main()
