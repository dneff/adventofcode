"""
Advent of Code 2017 - Day 19: A Series of Tubes (Part 2)

Part 2 asks for the total number of steps taken by the packet as it follows
the routing diagram from start to finish. This includes every move made,
whether passing through a path segment, a corner, or a letter marker.

The goal is to count how many steps the packet needs to take to reach the end.
"""
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/19/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def main():
    """Follow the routing diagram and count total steps taken."""
    lines = AoCInput.read_lines(INPUT_FILE)

    # Build a dictionary of all non-space positions in the routing diagram
    routing_diagram = {}
    for y, line in enumerate(lines):
        for x, point in enumerate([*line]):
            if point != ' ':
                routing_diagram[(x, y)] = point

    # Direction vectors: down, left, up, right (indexed 0-3)
    directions = [(0, 1), (-1, 0), (0, -1), (1, 0)]
    # Expected path character when turning (horizontal for vertical travel, vice versa)
    expected_turn_char = [('-'), ('|'), ('-'), ('|')]

    # Start at position (1, 0) heading down
    position = (1, 0)
    heading = 0  # 0=down, 1=left, 2=up, 3=right
    step_count = 0
    collected_letters = ''

    # Follow the path until we step off the diagram
    while position in routing_diagram:
        if routing_diagram[position] in ['|', '-']:
            # Continue straight on path segments
            pass
        elif routing_diagram[position] == '+':
            # Corner: must turn left or right
            new_path_char = expected_turn_char[heading]
            # Next position is either left or right of current heading
            left = (heading - 1) % 4
            left_x, left_y  = position[0] + directions[left][0], position[1] + directions[left][1]
            right = (heading + 1) % 4

            # Turn toward whichever side has the expected path character
            if (left_x, left_y) in routing_diagram and routing_diagram[(left_x, left_y)] == new_path_char:
                heading = left
            else:
                heading = right
        else:
            # Letter marker - collect it
            collected_letters = collected_letters + routing_diagram[position]

        # Move forward in current heading and count the step
        x, y = position[0] + directions[heading][0], position[1] + directions[heading][1]
        position = (x, y)
        step_count += 1

    AoCUtils.print_solution(2, step_count)


if __name__ == "__main__":
    main()
