"""
Advent of Code 2019 - Day 1: The Tyranny of the Rocket Equation
Part 1: Calculate basic fuel requirements for all spacecraft modules.

The Fuel Counter-Upper needs to know the total fuel requirement. To find it,
individually calculate the fuel needed for the mass of each module (your puzzle input),
then add together all the fuel values.

Fuel formula: Take mass, divide by 3, round down, subtract 2.
"""
import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/1/input')


def calculate_module_fuel(mass):
    """
    Calculate fuel required for a module's mass.

    Formula: fuel = (mass // 3) - 2

    Args:
        mass: The mass of the module

    Returns:
        The fuel required for this module
    """
    return (mass // 3) - 2


def solve_part1():
    """Calculate total fuel required for all spacecraft modules."""
    lines = AoCInput.read_lines(INPUT_FILE)
    total_fuel_required = 0

    for line in lines:
        module_mass = int(line.strip())
        total_fuel_required += calculate_module_fuel(module_mass)

    return total_fuel_required


answer = solve_part1()
AoCUtils.print_solution(1, answer)
