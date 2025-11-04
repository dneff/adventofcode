"""
Advent of Code 2018 - Day 11: Chronal Charge
https://adventofcode.com/2018/day/11

Find the optimal square of any size within a 300x300 grid of fuel cells that maximizes
total power. Each fuel cell's power level is calculated using a specific algorithm.

Part 2: Find the X,Y,size identifier of the square with the largest total power, where
size can be any value from 1 to 300.

This solution uses a summed-area table (integral image) for efficient calculation of
square sums of arbitrary sizes.
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
    power_level = (power_level // 100) % 10
    power_level -= 5

    return power_level


def build_summed_area_table(grid):
    """
    Build a summed-area table (integral image) for efficient range sum queries.

    The summed-area table allows calculating the sum of any rectangular region
    in O(1) time after O(n^2) preprocessing.

    Args:
        grid: Dictionary mapping (x, y) to power levels

    Returns:
        dict: Summed-area table where each cell contains the sum of all cells
              above and to the left (inclusive)
    """
    sat = {}

    for x in range(1, 301):
        for y in range(1, 301):
            # Current cell value
            value = grid[(x, y)]

            # Add sum from cell above
            if y > 1:
                value += sat[(x, y - 1)]

            # Add sum from cell to the left
            if x > 1:
                value += sat[(x - 1, y)]

            # Subtract the overlap (added twice)
            if x > 1 and y > 1:
                value -= sat[(x - 1, y - 1)]

            sat[(x, y)] = value

    return sat


def get_square_power(sat, x, y, size):
    """
    Calculate the total power of a square using the summed-area table.

    Uses the inclusion-exclusion principle:
    sum = bottom_right - top_right - bottom_left + top_left

    Args:
        sat: Summed-area table
        x: X coordinate of top-left cell
        y: Y coordinate of top-left cell
        size: Size of the square

    Returns:
        int: Total power of the square, or 0 if out of bounds
    """
    # Check bounds
    if x < 1 or y < 1 or x + size - 1 > 300 or y + size - 1 > 300:
        return 0

    # Bottom-right corner
    se = sat.get((x + size - 1, y + size - 1), 0)

    # Top-right corner (exclude)
    ne = sat.get((x + size - 1, y - 1), 0)

    # Bottom-left corner (exclude)
    sw = sat.get((x - 1, y + size - 1), 0)

    # Top-left corner (include back, was excluded twice)
    nw = sat.get((x - 1, y - 1), 0)

    return se - ne - sw + nw


def solve_part2():
    """
    Find the square of any size with the largest total power.

    Returns:
        str: "X,Y,size" identifier of the optimal square
    """
    # Read grid serial number from input
    serial_number = int(AoCInput.read_lines(INPUT_FILE)[0].strip())

    # Calculate power level for each cell
    grid = {}
    for x in range(1, 301):
        for y in range(1, 301):
            grid[(x, y)] = calculate_power_level(x, y, serial_number)

    # Build summed-area table for efficient square sum calculation
    sat = build_summed_area_table(grid)

    # Find the optimal square across all sizes
    max_power = float('-inf')
    best_config = None

    for size in range(1, 301):
        # Find best position for this size
        for x in range(1, 302 - size):
            for y in range(1, 302 - size):
                power = get_square_power(sat, x, y, size)
                if power > max_power:
                    max_power = power
                    best_config = (x, y, size)

    return f"{best_config[0]},{best_config[1]},{best_config[2]}"


# Compute and print the answer
answer = solve_part2()
AoCUtils.print_solution(2, answer)