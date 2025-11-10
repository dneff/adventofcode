"""
Advent of Code 2019 - Day 12: The N-Body Problem - Part 1

Simulate the motion of four moons orbiting Jupiter under gravity. Each moon has
a position and velocity in 3D space. Simulate for 1000 steps and calculate the
total system energy (sum of each moon's potential energy * kinetic energy).
"""
import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402
from Point import Point  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/12/input')


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


def solve_part1():
    """Simulate moon system for 1000 steps and calculate total energy."""
    lines = AoCInput.read_lines(INPUT_FILE)
    moons = parse_moon_positions(lines)

    simulation_steps = 1000
    for _ in range(simulation_steps):
        simulate_gravity_step(moons)

    total_energy = sum(moon.getEnergy() for moon in moons)
    return total_energy


answer = solve_part1()
AoCUtils.print_solution(1, answer)
