"""
Advent of Code 2017 - Day 8: I Heard You Like Registers (Part 1)

Process a series of register instructions with conditional logic. Each instruction modifies
a register by increasing or decreasing its value if a specified condition is met. All
registers start at 0. Find the largest value in any register after completing all instructions.

Instruction format: <register> <inc|dec> <amount> if <register> <comparison> <value>

Example:
    b inc 5 if a > 1   # Increase b by 5 if a > 1
    a inc 1 if b < 5   # Increase a by 1 if b < 5
    c dec -10 if a >= 1  # Decrease c by -10 (i.e., increase by 10) if a >= 1
    c inc -20 if c == 10  # Increase c by -20 (i.e., decrease by 20) if c == 10

Supported comparison operators: >, <, >=, <=, ==, !=
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/8/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
from collections import defaultdict


class RegisterComputer():
    """A simple computer that processes conditional register modification instructions."""

    def __init__(self):
        self.instructions = []
        self.registers = defaultdict(int)

    def run(self):
        """Execute all instructions in sequence."""
        for instruction in self.instructions:
            self.execute_instruction(instruction)

    def execute_instruction(self, instruction):
        """
        Execute a single instruction if its condition is met.

        Args:
            instruction: List of instruction components [register, op, amount, 'if', cond_reg, comparison, cond_value]
        """
        target_register = instruction[0]
        operation = instruction[1]
        amount = int(instruction[2])
        condition_register = instruction[4]
        comparison_operator = instruction[5]
        condition_value = int(instruction[6])

        # Build and evaluate the condition
        condition = f"self.registers['{condition_register}'] {comparison_operator} {condition_value}"

        if eval(condition):
            # Execute the modification
            if operation == 'inc':
                self.registers[target_register] += amount
            else:  # dec
                self.registers[target_register] -= amount


def main():
    """Execute instructions and find the largest final register value."""
    computer = RegisterComputer()
    lines = AoCInput.read_lines(INPUT_FILE)

    for line in lines:
        computer.instructions.append(line.strip().split())

    computer.run()

    max_value = max(computer.registers.values())
    AoCUtils.print_solution(1, max_value)


if __name__ == "__main__":
    main()
