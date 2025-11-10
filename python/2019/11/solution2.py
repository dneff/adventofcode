"""
Advent of Code 2019 - Day 11: Space Police - Part 2

Run the painting robot again, but this time start on a white panel instead
of black. The robot will paint a registration identifier. After the robot
finishes, display the pattern of white panels to read the registration identifier.
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


def render_registration_identifier(hull_panels):
    """
    Render the painted hull as a registration identifier.

    Args:
        hull_panels: Dictionary mapping (x, y) -> color (0=black, 1=white)

    Returns:
        Multi-line string showing the registration identifier
    """
    white_panels = [pos for pos, color in hull_panels.items() if color == 1]

    if not white_panels:
        return "No white panels painted"

    max_y = max(pos[1] for pos in white_panels)
    max_x = max(pos[0] for pos in white_panels)

    # Build the display from top to bottom
    lines = []
    for y in range(max_y, -1, -1):
        row = []
        for x in range(max_x + 1):
            if (x, y) in white_panels:
                row.append('#')
            else:
                row.append(' ')
        lines.append(''.join(row))

    return '\n' + '\n'.join(lines)


def solve_part2():
    """Run the painting robot starting on a white panel to get registration ID."""
    program = AoCInput.read_file(INPUT_FILE).strip()

    # Initialize hull panel colors (default to black=0)
    hull_panels = defaultdict(int)
    robot_x, robot_y = 0, 5  # Start position (offset for display)
    hull_panels[(robot_x, robot_y)] = 1  # Start on WHITE panel

    # Robot state
    directions = ['N', 'E', 'S', 'W']
    robot_orientation = 0  # Start facing North
    expecting_turn_output = False  # Toggle between color and turn outputs

    # Initialize Intcode computer
    painting_robot = IntCode(program)
    painting_robot.push(hull_panels[(robot_x, robot_y)])

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

            expecting_turn_output = not expecting_turn_output

    return render_registration_identifier(hull_panels)


answer = solve_part2()
# Print the solution using OCR for better readability
solution = AoCUtils.ocr_screen_4x6(answer)
AoCUtils.print_solution(2, solution)