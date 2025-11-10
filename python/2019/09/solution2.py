"""
Advent of Code 2019 - Day 9: Sensor Boost - Part 2

Run the BOOST program in sensor boost mode (input=2) to activate the distress
signal and obtain the coordinates. This uses the same enhanced Intcode computer
from Part 1 but with different input.
"""
import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from IntCode import IntCode, OutputInterrupt  # noqa: E402
from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/9/input')


def run_boost_sensor_mode(program):
    """
    Run the BOOST program in sensor boost mode.

    Args:
        program: The BOOST Intcode program as a string

    Returns:
        The coordinates of the distress signal
    """
    computer = IntCode(program)
    computer.push(2)  # Input value 2 for sensor boost mode

    # Run until program completes
    while not computer.complete:
        try:
            computer.run()
        except OutputInterrupt:
            # Continue running after each output
            pass

    # Return the last output value (the coordinates)
    return computer.output[-1]


def solve_part2():
    """Run BOOST in sensor boost mode and return the coordinates."""
    program = AoCInput.read_file(INPUT_FILE).strip()
    return run_boost_sensor_mode(program)


answer = solve_part2()
AoCUtils.print_solution(2, answer)
