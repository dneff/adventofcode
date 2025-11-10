"""
Advent of Code 2019 - Day 1: The Tyranny of the Rocket Equation
Part 2: Calculate fuel requirements accounting for the mass of the fuel itself.

Fuel itself requires fuel just like a module - take its mass, divide by three,
round down, and subtract 2. However, that fuel ALSO requires fuel, and that fuel
requires fuel, and so on. Any mass that would require negative fuel should instead
be treated as if it requires zero fuel.

Calculate the fuel requirements for each module separately, then add them all up
at the end.
"""
import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/1/input')


def calculate_module_fuel_recursive(mass):
    """
    Calculate fuel required for a module's mass, accounting for the fuel's mass.

    Recursively calculates fuel needed:
    1. Calculate fuel for the given mass
    2. Calculate fuel for that fuel
    3. Continue until additional fuel would be negative or zero

    Args:
        mass: The mass of the module

    Returns:
        The total fuel required (including fuel for the fuel)
    """
    total_fuel = 0
    fuel = (mass // 3) - 2

    # Keep adding fuel for the fuel until it becomes non-positive
    while fuel > 0:
        total_fuel += fuel
        fuel = (fuel // 3) - 2

    return total_fuel


def solve_part2():
    """Calculate total fuel required for all modules, accounting for fuel mass."""
    lines = AoCInput.read_lines(INPUT_FILE)
    total_fuel_required = 0

    for line in lines:
        module_mass = int(line.strip())
        total_fuel_required += calculate_module_fuel_recursive(module_mass)

    return total_fuel_required


answer = solve_part2()
AoCUtils.print_solution(2, answer)
