"""
Advent of Code 2018 - Day 10: The Stars Align
https://adventofcode.com/2018/day/10

Points of light in the sky move according to their velocities. After a certain number of
seconds, they align to form readable text.

Part 1: Determine what message will eventually appear in the sky.
Part 2: Determine how many seconds it takes for the message to appear.
"""

import os
import sys
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2018/10/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


class Star:
    """Represents a point of light with position and velocity."""

    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def move(self):
        """Move the star one time step forward."""
        self.x += self.vx
        self.y += self.vy

    def move_back(self):
        """Move the star one time step backward."""
        self.x -= self.vx
        self.y -= self.vy

    @property
    def position(self):
        """Get current position as a tuple."""
        return (self.x, self.y)


def parse_stars(lines):
    """
    Parse star positions and velocities from input lines.

    Args:
        lines: List of input lines in format "position=<x, y> velocity=<vx, vy>"

    Returns:
        list: List of Star objects
    """
    stars = []
    for line in lines:
        # Extract numbers from format: position=<10, -3> velocity=<-1, 1>
        matches = re.findall(r'<([^>]+)>', line)
        pos_parts = matches[0].split(', ')
        vel_parts = matches[1].split(', ')

        x, y = int(pos_parts[0]), int(pos_parts[1])
        vx, vy = int(vel_parts[0]), int(vel_parts[1])

        stars.append(Star(x, y, vx, vy))

    return stars


def get_bounding_box_height(stars):
    """
    Calculate the height of the bounding box containing all stars.

    Args:
        stars: List of Star objects

    Returns:
        int: Height of bounding box (max_y - min_y)
    """
    y_coords = [star.y for star in stars]
    return max(y_coords) - min(y_coords)


def render_message(stars):
    """
    Render the star positions as a visual message.

    Args:
        stars: List of Star objects

    Returns:
        str: Multi-line string showing the message
    """
    positions = set(star.position for star in stars)

    min_x = min(star.x for star in stars)
    max_x = max(star.x for star in stars)
    min_y = min(star.y for star in stars)
    max_y = max(star.y for star in stars)

    lines = []
    for y in range(min_y, max_y + 1):
        line = ''
        for x in range(min_x, max_x + 1):
            line += '#' if (x, y) in positions else ' '
        lines.append(line)

    return '\n'.join(lines)


def solve():
    """
    Find when the stars align to form a message.

    The message appears when the stars are most tightly packed (minimum bounding box).
    We simulate forward until the bounding box starts expanding again.

    Returns:
        tuple: (message_string, seconds_elapsed)
    """
    lines = AoCInput.read_lines(INPUT_FILE)
    stars = parse_stars(lines)

    # Find the moment when stars are most tightly packed
    height = get_bounding_box_height(stars)
    seconds = 0

    while True:
        # Move all stars one step forward
        for star in stars:
            star.move()

        seconds += 1
        new_height = get_bounding_box_height(stars)

        # If height is increasing, we've passed the alignment point
        if new_height > height:
            # Move back one step to the alignment point
            for star in stars:
                star.move_back()
            seconds -= 1
            break

        height = new_height

    # Render the message
    message = render_message(stars)

    return message, seconds


# Compute and display the solution
message, seconds = solve()

print("Part 1 - The message that appears:")
print(message)
print()
AoCUtils.print_solution(2, seconds)