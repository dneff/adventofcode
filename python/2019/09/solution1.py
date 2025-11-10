"""
Advent of Code 2019 - Day 9: Sensor Boost - Part 1

Run the BOOST program in test mode (input=1) to verify the enhanced Intcode computer.
This part requires implementing:
- Relative mode parameters (mode 2)
- Relative base adjustment (opcode 9)
- Extended memory support

The program outputs a BOOST keycode if all opcodes work correctly.
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


def run_boost_test_mode(program):
    """
    Run the BOOST program in test mode.

    Args:
        program: The BOOST Intcode program as a string

    Returns:
        The BOOST keycode output by the program
    """
    computer = IntCode(program)
    computer.push(1)  # Input value 1 for test mode

    # Run until program completes
    while not computer.complete:
        try:
            computer.run()
        except OutputInterrupt:
            # Continue running after each output
            pass

    return computer.pop()


def solve_part1():
    """Run BOOST in test mode and return the keycode."""
    program = AoCInput.read_file(INPUT_FILE).strip()
    return run_boost_test_mode(program)


answer = solve_part1()
AoCUtils.print_solution(1, answer)
