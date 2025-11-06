"""
Advent of Code 2017 - Day 19: A Series of Tubes (Part 1)

A network packet follows a routing diagram made of ASCII art. The diagram uses:
- '|' and '-' for straight paths
- '+' for corners where the packet must turn
- Letters (A-Z) as markers along the path

Starting at the top (entrance), the packet follows the path collecting letters
in the order it encounters them until reaching the end.

The goal is to determine the sequence of letters the packet sees along its path.
"""
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/19/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402


def build_routing_diagram(lines):
    """Build a dictionary of all non-space positions in the routing diagram.

    Args:
        lines: List of strings representing the routing diagram

    Returns:
        Dictionary mapping (x, y) coordinates to characters
    """
    routing_diagram = {}
    for y, line in enumerate(lines):
        for x, point in enumerate([*line]):
            if point != ' ':
                routing_diagram[(x, y)] = point
    return routing_diagram


def find_new_direction(position, heading, directions, routing_diagram):
    """Find the new direction to turn at a corner.

    Args:
        position: Current (x, y) position
        heading: Current heading (0=down, 1=left, 2=up, 3=right)
        directions: List of direction vectors
        routing_diagram: Dictionary of diagram positions

    Returns:
        New heading direction

    Raises:
        RuntimeError: If no valid turn is found
    """
    reverse = (heading + 2) % 4  # Opposite direction (where we came from)

    for new_heading in range(4):
        if new_heading == reverse:
            continue  # Don't go backwards

        new_x = position[0] + directions[new_heading][0]
        new_y = position[1] + directions[new_heading][1]
        next_char = routing_diagram.get((new_x, new_y), '')

        # Valid path if there's any non-space character
        if next_char and next_char != ' ':
            return new_heading

    raise RuntimeError("No valid turn found at corner!")


def main():
    """Follow the routing diagram and collect letters encountered along the path."""
    # Read lines preserving leading spaces (they're significant for positioning)
    lines = AoCInput.read_lines(INPUT_FILE, preserve_leading_space=True)

    # Build routing diagram
    routing_diagram = build_routing_diagram(lines)

    # Direction vectors: down, left, up, right (indexed 0-3)
    directions = [(0, 1), (-1, 0), (0, -1), (1, 0)]

    # Find the starting position on the first line (y=0)
    start_x = lines[0].index('|')
    position = (start_x, 0)
    heading = 0  # 0=down, 1=left, 2=up, 3=right

    collected_letters = ''
    # Follow the path until we step off the diagram
    while position in routing_diagram:
        current_char = routing_diagram[position]

        if current_char in ['|', '-']:
            # Continue straight on path segments
            pass
        elif current_char == '+':
            # Corner: find new direction
            heading = find_new_direction(position, heading, directions, routing_diagram)
        else:
            # Letter marker - collect it
            collected_letters = collected_letters + routing_diagram[position]

        # Move forward in current heading
        x, y = position[0] + directions[heading][0], position[1] + directions[heading][1]
        position = (x, y)

    AoCUtils.print_solution(1, collected_letters)


if __name__ == "__main__":
    main()
