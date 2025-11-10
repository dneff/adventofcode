"""
Advent of Code 2019 - Day 11: Space Police - Part 1

Build an emergency hull painting robot controlled by an Intcode program.
The robot starts on a black panel and:
1. Reads the current panel color (0=black, 1=white)
2. Outputs a color to paint (0=black, 1=white)
3. Outputs a turn direction (0=left 90°, 1=right 90°)
4. Moves forward one panel

Count how many panels the robot paints at least once.
"""
import os
import sys
from collections import defaultdict

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402
from IntCode import IntCode, InputInterrupt, OutputInterrupt  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/11/input')


def turn_robot(current_orientation, turn_direction):
    """
    Turn the robot left or right from its current orientation.

    Args:
        current_orientation: Index in ['N', 'E', 'S', 'W'] (0-3)
        turn_direction: 0 for left, 1 for right

    Returns:
        New orientation index
    """
    if turn_direction == 0:  # Turn left
        return (current_orientation - 1) % 4
    else:  # Turn right (1)
        return (current_orientation + 1) % 4


def move_forward(position, direction_name):
    """
    Move one step forward in the given direction.

    Args:
        position: Current (x, y) position
        direction_name: Direction name ('N', 'E', 'S', 'W')

    Returns:
        New (x, y) position
    """
    direction_deltas = {
        'N': (0, 1),
        'E': (1, 0),
        'S': (0, -1),
        'W': (-1, 0)
    }

    delta_x, delta_y = direction_deltas[direction_name]
    return position[0] + delta_x, position[1] + delta_y


def solve_part1():
    """Run the painting robot and count panels painted at least once."""
    program = AoCInput.read_file(INPUT_FILE).strip()

    # Initialize hull panel colors (default to black=0)
    hull_panels = defaultdict(int)
    robot_x, robot_y = 0, 0
    hull_panels[(robot_x, robot_y)] = 0

    # Robot state
    directions = ['N', 'E', 'S', 'W']
    robot_orientation = 0  # Start facing North
    expecting_turn_output = False  # Toggle between color and turn outputs

    # Initialize Intcode computer
    painting_robot = IntCode(program)
    painting_robot.push(hull_panels[(robot_x, robot_y)])

    panels_painted = set()

    while not painting_robot.complete:
        try:
            painting_robot.run()
        except InputInterrupt:
            # Robot needs current panel color
            current_color = hull_panels[(robot_x, robot_y)]
            painting_robot.push(current_color)
        except OutputInterrupt:
            output_value = painting_robot.pop()

            if expecting_turn_output:
                # This output is turn direction
                robot_orientation = turn_robot(robot_orientation, output_value)
                robot_x, robot_y = move_forward((robot_x, robot_y), directions[robot_orientation])
            else:
                # This output is paint color
                hull_panels[(robot_x, robot_y)] = output_value
                panels_painted.add((robot_x, robot_y))

            expecting_turn_output = not expecting_turn_output

    return len(panels_painted)


answer = solve_part1()
AoCUtils.print_solution(1, answer)
