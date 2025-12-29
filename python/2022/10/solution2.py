"""
Advent of Code 2022 - Day 10, Part 2
https://adventofcode.com/2022/day/10

This script simulates a CRT display driven by CPU instructions.
"""

import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2022/10/input')


class Device:
    """Simulates a CPU with CRT display."""

    def __init__(self):
        self.instructions = []
        self.cycle = 0
        self.index = 0
        self.X = 1
        row = [' '] * 40
        self.CRT = [row.copy() for _ in range(6)]

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

    def is_drawn(self):
        """Check if current pixel should be drawn."""
        position = self.cycle % 40
        return self.X in [position, position + 1, position - 1]

    def draw(self):
        """Draw a pixel on the CRT."""
        row = self.cycle // 40
        col = self.cycle % 40
        self.CRT[row][col] = '#'

    def add_cycle(self):
        """Increment cycle counter and update CRT display."""
        if self.is_drawn():
            self.draw()
        self.cycle = self.cycle + 1
        if self.cycle == 241:
            self.cycle = 1

    def run(self):
        """Execute all instructions."""
        while self.index < len(self.instructions):
            instruction = self.instructions[self.index]
            if instruction == 'noop':
                self.noop()
            elif instruction.startswith('addx'):
                value = int(instruction.split()[1])
                self.addx(value)


def solve_part2():
    """
    Simulate CPU and display the CRT output.
    """
    lines = AoCInput.read_lines(INPUT_FILE)
    device = Device()
    device.instructions = lines
    device.run()

    # Print the CRT display
    for row in device.CRT:
        print(''.join(row))
    print()


# Execute and display the CRT output
solve_part2()
