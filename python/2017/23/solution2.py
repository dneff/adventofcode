"""
Advent of Code 2017 - Day 23: Coprocessor Conflagration (Part 2)

Part 2 asks what value would be in register 'h' after the program completes
if register 'a' starts at 1 instead of 0.

Running the program directly would take too long. Through analysis/debugging,
the program is found to count composite (non-prime) numbers in a specific range.

The optimized solution checks which numbers in the range [106500, 106500+1000*17]
with step 17 are composite (not prime).
"""
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/23/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402
from collections import defaultdict  # noqa: E402
from string import ascii_lowercase as letters  # noqa: E402
from sympy import isprime  # noqa: E402


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
        """Execute instructions until the program terminates (for debugging only).

        This method includes debug print statements that are commented out in production.
        """
        while -1 < self.pointer < len(self.program):
            instruction = self.program[self.pointer]
            # Uncomment for debugging:
            # print(f"pc{self.id}:{self.pointer} - {instruction[0]} - {instruction[1]} "
            #       f"({self.get(instruction[1])}) - {instruction[2]} - ({self.get(instruction[2])})")
            method = getattr(self, instruction[0])
            method(*instruction[1:],)
            if instruction[0] != 'jnz':
                self.pointer += 1
            if self.halted:
                return
            # Uncomment for debugging:
            # print(f"register b, d, e: {self.registers['b']} {self.registers['d']} {self.registers['e']}")

        self.halted = True
        return

    def set(self, x, y):
        """Set register X to the value of Y."""
        self.registers[x] = self.get(y)

    def sub(self, x, y):
        """Decrease register X by the value of Y."""
        self.registers[x] -= self.get(y)

    def mul(self, x, y):
        """Multiply register X by the value of Y."""
        self.registers[x] *= self.get(y)
        self.mul_count += 1

    def jnz(self, x, y):
        """Jump by offset Y if X is not zero."""
        if self.get(x) != 0:
            self.pointer += self.get(y)
        else:
            self.pointer += 1

    def get(self, x):
        """Get the value of x, either from a register or as a literal integer."""
        if x in letters:
            return self.registers[x]
        else:
            return int(x)


def main():
    """Solve Part 2 using optimized prime-checking instead of running the slow program."""
    processor = Coprocessor(0)
    processor.registers['a'] = 1

    lines = AoCInput.read_lines(INPUT_FILE)

    for line in lines:
        processor.program.append(line.strip().split())

    # The program would be extremely slow to run directly.
    # After debugging/analysis, it counts composite numbers in a specific range.
    # Optimized solution:
    test_value = 106500  # Starting value (specific to puzzle input)
    composite_count = 0

    # Check 1001 numbers in the sequence: 106500, 106517, 106534, ...
    for x in range(1001):
        if not isprime(test_value):
            composite_count += 1
        test_value += 17

    AoCUtils.print_solution(2, composite_count)


if __name__ == "__main__":
    main()
