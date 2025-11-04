"""
Advent of Code 2018 - Day 11: Chronal Charge
https://adventofcode.com/2018/day/11

Find the optimal 3x3 square within a 300x300 grid of fuel cells that maximizes total power.
Each fuel cell's power level is calculated using a specific algorithm involving the rack ID
(X + 10), the grid serial number, and extracting the hundreds digit.

Part 1: Find the X,Y coordinate of the top-left fuel cell of the 3x3 square with the largest
total power.
"""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2018/11/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def calculate_power_level(x, y, serial_number):
    """
    Calculate the power level of a fuel cell at position (x, y).

    Algorithm:
    1. Rack ID = X + 10
    2. Power level = rack_id * Y
    3. Power level += serial_number
    4. Power level *= rack_id
    5. Extract hundreds digit
    6. Subtract 5

    Args:
        x: X coordinate (1-300)
        y: Y coordinate (1-300)
        serial_number: Grid serial number

    Returns:
        int: Power level of the fuel cell
    """
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial_number
    power_level *= rack_id
    # Extract hundreds digit: divide by 100 and take remainder when divided by 10
    power_level = (power_level // 100) % 10
    power_level -= 5

    return power_level


def calculate_3x3_power(grid, x, y):
    """
    Calculate the total power of a 3x3 square with top-left at (x, y).

    Args:
        grid: Dictionary mapping (x, y) to power levels
        x: X coordinate of top-left cell
        y: Y coordinate of top-left cell

    Returns:
        int: Total power of the 3x3 square
    """
    total_power = 0
    for dx in range(3):
        for dy in range(3):
            total_power += grid[(x + dx, y + dy)]

    return total_power


def solve_part1():
    """
    Find the 3x3 square with the largest total power.

    Returns:
        tuple: (x, y) coordinates of the top-left cell
    """
    # Read grid serial number from input
    serial_number = int(AoCInput.read_lines(INPUT_FILE)[0].strip())

    # Calculate power level for each cell in the 300x300 grid
    grid = {}
    for x in range(1, 301):
        for y in range(1, 301):
            grid[(x, y)] = calculate_power_level(x, y, serial_number)

    # Find the 3x3 square with maximum total power
    max_power = float('-inf')
    best_position = None

    # Check all possible 3x3 squares (top-left can be at most 298, 298)
    for x in range(1, 299):
        for y in range(1, 299):
            power = calculate_3x3_power(grid, x, y)
            if power > max_power:
                max_power = power
                best_position = (x, y)

    return best_position


# Compute and print the answer
answer = solve_part1()
AoCUtils.print_solution(1, f"{answer[0]},{answer[1]}")