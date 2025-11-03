"""
Advent of Code 2017 - Day 23: Coprocessor Conflagration (Part 1)

Debug an experimental coprocessor running a simple assembly program.
The program uses four instructions: set, sub, mul, and jnz.
All eight registers (a-h) start at 0.

Instructions:
- set X Y: assigns Y's value to register X
- sub X Y: decreases register X by Y's value
- mul X Y: multiplies register X by Y's value
- jnz X Y: jumps by Y's offset if X is not zero

The goal is to count how many times the 'mul' instruction is executed.
"""
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/23/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
from collections import defaultdict
from string import ascii_lowercase as letters


class Coprocessor():
    """Simulates a simple coprocessor with registers and basic instructions."""
    def __init__(self, program_id):
        self.id = program_id
        self.duet = None  # For compatibility (unused in this puzzle)
        self.program = []
        self.buffer = []  # For compatibility (unused in this puzzle)
        self.tx_count = 0  # For compatibility (unused in this puzzle)
        self.mul_count = 0  # Count mul instruction invocations
        self.pointer = 0  # Instruction pointer
        self.halted = False  # True when program terminates
        self.registers = defaultdict(int)

    def run(self):
        """Execute instructions until the program terminates.

        Runs instructions sequentially until the instruction pointer
        goes out of bounds.
        """
        while -1 < self.pointer < len(self.program):
            instruction = self.program[self.pointer]
            method = getattr(self, instruction[0])
            method(*instruction[1:],)
            if instruction[0] != 'jnz':
                self.pointer += 1
            if self.halted == True:
                return
        self.halted = True
        return

    def set(self, x, y):
        """Set register X to the value of Y.

        Args:
            x: Register name
            y: Register name or literal value
        """
        self.registers[x] = self.get(y)

    def sub(self, x, y):
        """Decrease register X by the value of Y.

        Args:
            x: Register name
            y: Register name or literal value
        """
        self.registers[x] -= self.get(y)

    def mul(self, x, y):
        """Multiply register X by the value of Y and count the invocation.

        Args:
            x: Register name
            y: Register name or literal value
        """
        self.registers[x] *= self.get(y)
        self.mul_count += 1

    def jnz(self, x, y):
        """Jump by offset Y if X is not zero.

        Args:
            x: Register name or literal value to test
            y: Register name or literal value for jump offset
        """
        if self.get(x) != 0:
            self.pointer += self.get(y)
        else:
            self.pointer += 1

    def get(self, x):
        """Get the value of x, either from a register or as a literal integer.

        Args:
            x: Either a register name (letter) or a string representation of an integer

        Returns:
            The integer value from the register or the literal value
        """
        if x in letters:
            return self.registers[x]
        else:
            return int(x)


def main():
    """Run the coprocessor program and count mul instruction invocations."""
    processor = Coprocessor(0)

    lines = AoCInput.read_lines(INPUT_FILE)

    for line in lines:
        processor.program.append(line.strip().split())

    while not processor.halted:
        processor.run()

    AoCUtils.print_solution(1, processor.mul_count)


if __name__ == "__main__":
    main()
