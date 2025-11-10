"""
Advent of Code 2019 - Day 3: Crossed Wires
Part 2: Find the intersection with the fewest combined steps.

Instead of distance, calculate the total number of steps each wire takes to
reach each intersection. Find the intersection where the sum of both wires'
steps is minimized.
"""
import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/3/input')


def trace_wire_path(path_instructions):
    """
    Trace the path of a wire step by step, yielding each position.

    Args:
        path_instructions: List of directional moves like ['R8', 'U5', 'L5', 'D3']

    Yields:
        Each (x, y) position the wire passes through
    """
    position = [0, 0]  # Start at central port

    for instruction in path_instructions:
        direction = instruction[0]
        distance = int(instruction[1:])

        # Move step by step in the given direction
        for _ in range(distance):
            if direction == 'L':
                position[0] -= 1
            elif direction == 'R':
                position[0] += 1
            elif direction == 'U':
                position[1] += 1
            elif direction == 'D':
                position[1] -= 1

            yield tuple(position)


def solve_part2():
    """
    Find the intersection with the fewest combined steps from both wires.

    For each intersection, count:
    - Steps for wire 1 to reach the intersection
    - Steps for wire 2 to reach the intersection
    - Sum these to get total combined steps

    Returns:
        The minimum combined steps to any intersection
    """
    lines = AoCInput.read_lines(INPUT_FILE)
    wire1_path = lines[0].strip().split(',')
    wire2_path = lines[1].strip().split(',')

    # Get all positions each wire visits (in order)
    wire1_positions = list(trace_wire_path(wire1_path))
    wire2_positions = list(trace_wire_path(wire2_path))

    # Find intersections (points both wires visit)
    intersections = set(wire1_positions) & set(wire2_positions)

    # For each intersection, calculate combined steps
    combined_steps = []
    for intersection in intersections:
        # Find the first occurrence index (step count) in each wire's path
        # Add 1 to each because list indices start at 0 but steps start at 1
        wire1_steps = wire1_positions.index(intersection) + 1
        wire2_steps = wire2_positions.index(intersection) + 1

        combined_steps.append(wire1_steps + wire2_steps)

    return min(combined_steps)


answer = solve_part2()
AoCUtils.print_solution(2, answer)
