"""
Advent of Code 2018 - Day 13: Mine Cart Madness
https://adventofcode.com/2018/day/13

Simulate carts moving on tracks. Carts navigate straight paths, curves, and intersections
with specific turning rules at intersections (left, straight, right, repeating in that order).

Part 1: Find the location of the first crash.
"""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2018/13/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


class Cart:
    """Represents a mine cart moving on tracks."""

    # Direction indices: 0=Up, 1=Right, 2=Down, 3=Left
    ICONS = ['^', '>', 'v', '<']
    DIRECTIONS = ['U', 'R', 'D', 'L']

    def __init__(self, icon, location):
        self.direction = self.ICONS.index(icon)
        self.location = tuple(location)
        self.intersection_state = -1  # Cycles through -1, 0, 1 for left, straight, right

        # Movement deltas for each direction
        self.step_map = {
            'U': (0, -1),
            'R': (1, 0),
            'D': (0, 1),
            'L': (-1, 0)
        }

    def move(self, track_grid):
        """
        Move the cart one step, handling curves and intersections.

        Args:
            track_grid: Dictionary mapping (x, y) to track characters
        """
        current_track = track_grid[self.location]

        # Handle curves
        if current_track == '\\':
            # Backslash curve: vertical↔horizontal
            if self.direction % 2 == 0:  # Vertical (up/down)
                self.direction -= 1  # Turn left (up→left, down→right)
            else:  # Horizontal (right/left)
                self.direction += 1  # Turn right (right→down, left→up)

        elif current_track == '/':
            # Forward slash curve: vertical↔horizontal (opposite of backslash)
            if self.direction % 2 == 0:  # Vertical
                self.direction += 1  # Turn right (up→right, down→left)
            else:  # Horizontal
                self.direction -= 1  # Turn left (right→up, left→down)

        elif current_track == '+':
            # Intersection: turn left, go straight, or turn right
            self.direction += self.intersection_state % 4
            self.update_intersection_state()

        # Normalize direction to 0-3 range
        self.direction = self.direction % 4

        # Move forward
        heading = self.DIRECTIONS[self.direction]
        dx, dy = self.step_map[heading]
        self.location = (self.location[0] + dx, self.location[1] + dy)

    def update_intersection_state(self):
        """Update the intersection state for next intersection."""
        self.intersection_state += 1
        if self.intersection_state == 2:
            self.intersection_state = -1

    def __lt__(self, other):
        """Sort carts by position (top-to-bottom, left-to-right)."""
        if self.location[1] != other.location[1]:
            return self.location[1] < other.location[1]
        return self.location[0] < other.location[0]


def solve_part1():
    """
    Simulate cart movement and find the location of the first crash.

    Returns:
        str: "x,y" coordinates of the first crash
    """
    lines = AoCInput.read_lines(INPUT_FILE, preserve_leading_space=True)

    track_grid = {}
    carts = []

    # Parse the track layout and carts
    for y, line in enumerate(lines):
        for x, char in enumerate(line.rstrip('\n')):
            if char == ' ':
                continue

            if char in ['^', 'v']:
                # Vertical cart
                carts.append(Cart(char, (x, y)))
                track_grid[(x, y)] = '|'  # Replace with underlying track
            elif char in ['>', '<']:
                # Horizontal cart
                carts.append(Cart(char, (x, y)))
                track_grid[(x, y)] = '-'  # Replace with underlying track
            else:
                # Track piece
                track_grid[(x, y)] = char

    # Simulate until first crash
    while True:
        # Sort carts by position (top-to-bottom, left-to-right)
        carts.sort()

        for cart in carts:
            cart.move(track_grid)

            # Check for collision
            cart_positions = [c.location for c in carts]
            if len(set(cart_positions)) != len(cart_positions):
                # Found a crash
                return f"{cart.location[0]},{cart.location[1]}"


# Compute and print the answer
answer = solve_part1()
AoCUtils.print_solution(1, answer)