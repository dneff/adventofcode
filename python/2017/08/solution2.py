"""
Advent of Code 2017 - Day 8: I Heard You Like Registers (Part 2)

Process register instructions with conditional logic, but track the highest value held in
any register during the entire execution process (not just at the end). Find the maximum
value ever held across all registers throughout all instruction executions.

This requires tracking the peak value as instructions execute, since registers can be
modified multiple times and may decrease after reaching a high value.
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/8/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
from collections import defaultdict


class RegisterComputer():
    """A computer that processes conditional register instructions and tracks peak values."""

    def __init__(self):
        self.instructions = []
        self.registers = defaultdict(int)
        self.max_value_ever = 0

    def run(self):
        """Execute all instructions in sequence, tracking the maximum value."""
        for instruction in self.instructions:
            self.execute_instruction(instruction)

    def execute_instruction(self, instruction):
        """
        Execute a single instruction if its condition is met, updating max value tracker.

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

            # Track the maximum value ever held
            self.max_value_ever = max(self.max_value_ever, max(self.registers.values()))


def main():
    """Execute instructions and find the highest value ever held in any register."""
    computer = RegisterComputer()
    lines = AoCInput.read_lines(INPUT_FILE)

    for line in lines:
        computer.instructions.append(line.strip().split())

    computer.run()

    AoCUtils.print_solution(2, computer.max_value_ever)


if __name__ == "__main__":
    main()
