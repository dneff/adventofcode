"""
Advent of Code 2019 - Day 13: Care Package - Part 2

Play the arcade game by inserting 2 quarters (setting memory[0]=2) and beat the
game by moving the paddle to catch the ball. The joystick input is: -1 (left),
0 (neutral), 1 (right). Track the score which is output at position (-1, 0).
Return the final score after breaking all blocks.
"""
import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402
from IntCode import IntCode, OutputInterrupt, InputInterrupt  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/13/input')


def calculate_joystick_tilt(ball_position, paddle_position):
    """
    Determine joystick tilt to move paddle toward ball.

    Args:
        ball_position: (x, y) tuple of ball
        paddle_position: (x, y) tuple of paddle

    Returns:
        -1 (tilt left), 0 (neutral), or 1 (tilt right)
    """
    if ball_position[0] < paddle_position[0]:
        return -1  # Move paddle left
    elif ball_position[0] > paddle_position[0]:
        return 1  # Move paddle right
    else:
        return 0  # Keep paddle centered


def solve_part2():
    """Play the arcade game and return the final score."""
    program = AoCInput.read_file(INPUT_FILE).strip()

    # Track game state
    ball_position = (0, 0)
    paddle_position = (0, 0)
    final_score = 0

    # Initialize arcade computer in "free play" mode
    arcade_computer = IntCode(program)
    arcade_computer.memory[0] = 2  # Insert 2 quarters

    screen_tiles = {}

    while not arcade_computer.complete:
        try:
            arcade_computer.run()
        except InputInterrupt:
            # Provide joystick input to move paddle toward ball
            joystick_input = calculate_joystick_tilt(ball_position, paddle_position)
            arcade_computer.push(joystick_input)
        except OutputInterrupt:
            # Process output triplet (x, y, tile_id or score)
            if len(arcade_computer.output) == 3:
                x, y, value = arcade_computer.output

                if (x, y) == (-1, 0):
                    # Special position: score update
                    final_score = value
                elif value == 3:
                    # Paddle tile
                    paddle_position = (x, y)
                elif value == 4:
                    # Ball tile
                    ball_position = (x, y)

                screen_tiles[(x, y)] = value
                arcade_computer.output.clear()

    return final_score


answer = solve_part2()
AoCUtils.print_solution(2, answer)
