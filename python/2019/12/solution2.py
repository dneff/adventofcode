"""
Advent of Code 2019 - Day 12: The N-Body Problem - Part 2

Find how many steps it takes for the moon system to return to a previous state.
Since the system is deterministic, finding when each axis (x, y, z) repeats
independently, then calculating the LCM gives the full system repetition period.
"""
import os
import sys
from math import gcd

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402
from Point import Point  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/12/input')


def lcm(a, b):
    """Calculate least common multiple of two numbers."""
    return a * b // gcd(a, b)


def parse_moon_positions(lines):
    """
    Parse moon position data from input lines.

    Args:
        lines: Input lines in format "<x=..., y=..., z=...>"

    Returns:
        List of Point objects representing moons
    """
    moons = []
    for line in lines:
        coordinates = [int(coord.split('=')[-1])
                      for coord in line.strip().replace('<', '').replace('>', '').split(', ')]
        moons.append(Point(*coordinates))
    return moons


def simulate_gravity_step(moons):
    """
    Simulate one time step: apply gravity, then update positions.

    Args:
        moons: List of Point objects representing moons
    """
    # Apply gravity between all pairs of moons
    for i in range(len(moons)):
        for j in range(len(moons)):
            if i != j:
                moons[i].updateVelocity(moons[j])

    # Update all positions based on velocities
    for moon in moons:
        moon.updatePosition()


def solve_part2():
    """Find the number of steps until the system returns to initial state."""
    lines = AoCInput.read_lines(INPUT_FILE)
    moons = parse_moon_positions(lines)

    # Store initial state for each axis separately
    initial_x = sorted([(moon.pos_x, moon.vel_x) for moon in moons])
    initial_y = sorted([(moon.pos_y, moon.vel_y) for moon in moons])
    initial_z = sorted([(moon.pos_z, moon.vel_z) for moon in moons])

    # Find cycle length for each axis independently
    x_cycle = y_cycle = z_cycle = 0
    steps = 0

    while x_cycle == 0 or y_cycle == 0 or z_cycle == 0:
        steps += 1
        simulate_gravity_step(moons)

        # Check if x-axis has cycled
        if x_cycle == 0:
            current_x = sorted([(moon.pos_x, moon.vel_x) for moon in moons])
            if initial_x == current_x:
                x_cycle = steps

        # Check if y-axis has cycled
        if y_cycle == 0:
            current_y = sorted([(moon.pos_y, moon.vel_y) for moon in moons])
            if initial_y == current_y:
                y_cycle = steps

        # Check if z-axis has cycled
        if z_cycle == 0:
            current_z = sorted([(moon.pos_z, moon.vel_z) for moon in moons])
            if initial_z == current_z:
                z_cycle = steps

    # Full cycle is LCM of individual axis cycles
    return lcm(x_cycle, lcm(y_cycle, z_cycle))


answer = solve_part2()
AoCUtils.print_solution(2, answer)
