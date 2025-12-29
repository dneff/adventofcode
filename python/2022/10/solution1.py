"""
Advent of Code 2022 - Day 10: Cathode-Ray Tube
https://adventofcode.com/2022/day/10

This script simulates a CPU and calculates signal strength at specific cycles.
"""

import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2022/10/input')


class Device:
    """Simulates a simple CPU with cycle counting and signal strength tracking."""

    def __init__(self):
        self.instructions = []
        self.cycle = 0
        self.index = 0
        self.X = 1
        self.critical_cycles = {k: 0 for k in [20, 60, 100, 140, 180, 220]}

    def noop(self):
        """Execute a noop instruction."""
        self.add_cycle()
        self.index += 1

    def addx(self, value):
        """Execute an addx instruction."""
        self.add_cycle()
        self.add_cycle()
        self.X += value
        self.index += 1

    def signal_strength(self):
        """Calculate the signal strength for the current cycle."""
        return self.cycle * self.X

    def add_cycle(self):
        """Increment cycle counter and record signal strength at critical cycles."""
        self.cycle += 1
        if self.cycle in self.critical_cycles:
            self.critical_cycles[self.cycle] = self.signal_strength()

    def run(self):
        """Execute all instructions."""
        while self.index < len(self.instructions):
            instruction = self.instructions[self.index]
            if instruction == 'noop':
                self.noop()
            elif instruction.startswith('addx'):
                value = int(instruction.split()[1])
                self.addx(value)


def solve_part1():
    """
    Simulate CPU and calculate sum of signal strengths at critical cycles.

    Returns:
        int: Sum of signal strengths
    """
    lines = AoCInput.read_lines(INPUT_FILE)
    device = Device()
    device.instructions = lines
    device.run()
    return sum(device.critical_cycles.values())


# Compute and print the answer for part 1
answer = solve_part1()
AoCUtils.print_solution(1, answer)
