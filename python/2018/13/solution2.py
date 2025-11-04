"""
Advent of Code 2018 - Day 13: Mine Cart Madness
https://adventofcode.com/2018/day/13

Simulate carts moving on tracks. Carts navigate straight paths, curves, and intersections
with specific turning rules at intersections. When carts collide, they are removed from
the simulation.

Part 2: Find the location of the last remaining cart after all collisions.
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
        self.active = True  # Whether cart is still in simulation

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
            if self.direction % 2 == 0:  # Vertical
                self.direction -= 1
            else:  # Horizontal
                self.direction += 1

        elif current_track == '/':
            if self.direction % 2 == 0:  # Vertical
                self.direction += 1
            else:  # Horizontal
                self.direction -= 1

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


def solve_part2():
    """
    Simulate cart movement with collision removal until one cart remains.

    Returns:
        str: "x,y" coordinates of the last remaining cart
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
                carts.append(Cart(char, (x, y)))
                track_grid[(x, y)] = '|'
            elif char in ['>', '<']:
                carts.append(Cart(char, (x, y)))
                track_grid[(x, y)] = '-'
            else:
                track_grid[(x, y)] = char

    # Simulate until only one cart remains
    while len(carts) > 1:
        # Sort carts by position for this tick
        carts.sort()

        for cart in carts:
            if not cart.active:
                continue

            cart.move(track_grid)

            # Check for collision with other active carts
            active_positions = [c.location for c in carts if c.active]
            if len(set(active_positions)) != len(active_positions):
                # Mark all carts at this collision location as inactive
                for other_cart in carts:
                    if other_cart.location == cart.location:
                        other_cart.active = False

        # Remove inactive carts
        carts = [c for c in carts if c.active]

    # Return the location of the last remaining cart
    final_cart = carts[0]
    return f"{final_cart.location[0]},{final_cart.location[1]}"


# Compute and print the answer
answer = solve_part2()
AoCUtils.print_solution(2, answer)