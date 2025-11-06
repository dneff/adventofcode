"""
Advent of Code 2016 - Day 23: Safe Cracking
https://adventofcode.com/2016/day/23

Part 1: Execute assembunny code to crack the safe.
The safe's keypad uses assembunny code with a new instruction: toggle (tgl).
Starting with register 'a' initialized to 7, run the code and find the final value in register 'a'.

The assembunny computer supports these instructions:
- cpy x y: copies x (integer or register value) into register y
- inc x: increases register x by one
- dec x: decreases register x by one
- jnz x y: jumps y instructions away if x is not zero
- tgl x: toggles the instruction at position (current position + value of register x)
  - One-argument instructions: inc <-> dec, all others become inc
  - Two-argument instructions: jnz <-> cpy, all others become jnz

Performance Optimization:
This solution includes pattern detection to optimize nested loop structures that perform
multiplication operations. The pattern:
  cpy b c / inc a / dec c / jnz c -2 / dec d / jnz d -5
is recognized and replaced with a direct multiplication:
  a += b * d; c = 0; d = 0
This optimization reduces execution time from minutes to milliseconds by eliminating
millions of individual increment/decrement operations.
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/23/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402


class BunnyPC():
    """
    Assembunny computer interpreter for executing safe-cracking code.
    Supports basic assembunny instructions (cpy, inc, dec, jnz) plus the toggle (tgl) instruction.
    """

    def __init__(self):
        """Initialize the assembunny computer with four registers (a, b, c, d) and empty code."""
        self.register = {"a": 0, "b": 0, "c": 0, "d": 0}
        self.code = []  # List of assembunny instructions
        self.instruction_pointer = 0  # Current instruction being executed

    def load(self, filename):
        """Load assembunny code from input file."""
        lines = AoCInput.read_lines(filename)
        for line in lines:
            self.code.append(line.strip())

    def resolveX(self, x):
        """
        Resolve a value that could be either a register name or a literal integer.
        Returns the register's value if x is a register (a, b, c, or d), otherwise returns x as an integer.
        """
        if x in "abcd":
            return self.register[x]
        return int(x)

    def cpy(self, x, y):
        """Copy instruction: cpy x y copies x (integer or register value) into register y."""
        # Skip invalid cpy instructions (e.g., cpy 1 2 from toggles)
        if y not in "abcd":
            self.instruction_pointer += 1
            return
        self.register[y] = self.resolveX(x)
        self.instruction_pointer += 1

    def inc(self, x):
        """Increment instruction: inc x increases the value of register x by one."""
        # Skip invalid inc instructions (e.g., inc 1 from toggles)
        if x not in "abcd":
            self.instruction_pointer += 1
            return
        self.register[x] += 1
        self.instruction_pointer += 1

    def dec(self, x):
        """Decrement instruction: dec x decreases the value of register x by one."""
        # Skip invalid dec instructions (e.g., dec 1 from toggles)
        if x not in "abcd":
            self.instruction_pointer += 1
            return
        self.register[x] -= 1
        self.instruction_pointer += 1

    def mul(self, x, y, z):
        """
        Multiply instruction (optimization, not in original spec):
        mul x y z adds the product of y and z to register x.
        """
        self.register[x] += self.resolveX(y) * self.resolveX(z)
        self.instruction_pointer += 1

    def jnz(self, x, y):
        """
        Jump if not zero instruction: jnz x y jumps y instructions away if x is not zero.
        Positive y jumps forward, negative y jumps backward.
        """
        if self.resolveX(x) != 0:
            self.instruction_pointer += self.resolveX(y)
        else:
            self.instruction_pointer += 1

    def tgl(self, x):
        """
        Toggle instruction: tgl x toggles the instruction at offset (register x value) from current position.

        Toggle rules:
        - One-argument instructions: inc <-> dec, all others become inc
        - Two-argument instructions: jnz <-> cpy, all others become jnz
        - Arguments of toggled instructions are not affected
        - Toggling outside program bounds does nothing
        - Invalid instructions (e.g., cpy 1 2) are skipped during execution
        - If tgl toggles itself, the change takes effect on next execution
        """
        toggle_pointer = self.instruction_pointer + self.register[x]

        # Ignore toggle if target is out of bounds
        if toggle_pointer < 0 or toggle_pointer > (len(self.code) - 1):
            self.instruction_pointer += 1
            return

        # Parse and toggle the target instruction
        toggle_inst = self.code[toggle_pointer].split()
        if len(toggle_inst) == 2:  # One-argument instruction
            if toggle_inst[0] == 'inc':
                toggle_inst[0] = 'dec'
            else:
                toggle_inst[0] = 'inc'
        elif len(toggle_inst) == 3:  # Two-argument instruction
            if toggle_inst[0] == 'jnz':
                toggle_inst[0] = 'cpy'
            else:
                toggle_inst[0] = 'jnz'

        self.code[toggle_pointer] = ' '.join(toggle_inst)
        self.instruction_pointer += 1

    def detect_multiplication_pattern(self):
        """
        Detect and optimize multiplication patterns in the code.
        Pattern: cpy b c / inc a / dec c / jnz c -2 / dec d / jnz d -5
        This is equivalent to: a += b * d; c = 0; d = 0
        Returns True if pattern was detected and optimized.
        """
        ip = self.instruction_pointer
        # Check if we have enough instructions ahead
        if ip + 5 >= len(self.code):
            return False

        # Parse the next 6 instructions
        try:
            inst = [self.code[ip + i].split() for i in range(6)]
        except IndexError:
            return False

        # Pattern 1: cpy b c / inc a / dec c / jnz c -2 / dec d / jnz d -5
        if (len(inst[0]) == 3 and inst[0][0] == 'cpy' and
            len(inst[1]) == 2 and inst[1][0] == 'inc' and
            len(inst[2]) == 2 and inst[2][0] == 'dec' and
            len(inst[3]) == 3 and inst[3][0] == 'jnz' and inst[3][2] == '-2' and
            len(inst[4]) == 2 and inst[4][0] == 'dec' and
            len(inst[5]) == 3 and inst[5][0] == 'jnz' and inst[5][2] == '-5'):  # noqa: E129

            # Verify the pattern matches: cpy X Y / inc A / dec Y / jnz Y -2 / dec Z / jnz Z -5
            src_reg = inst[0][1]  # b
            temp_reg = inst[0][2]  # c
            dest_reg = inst[1][1]  # a
            loop_reg = inst[4][1]  # d

            if (inst[2][1] == temp_reg and inst[3][1] == temp_reg and
                inst[5][1] == loop_reg):  # noqa: E129
                # Execute the multiplication directly
                self.register[dest_reg] += self.resolveX(src_reg) * self.resolveX(loop_reg)
                self.register[temp_reg] = 0
                self.register[loop_reg] = 0
                self.instruction_pointer += 6
                return True

        return False

    def run(self):
        """
        Execute the loaded assembunny code until the instruction pointer exceeds the program bounds.
        Uses pattern detection to optimize multiplication loops.
        Returns the final value in register 'a'.
        """
        while self.instruction_pointer < len(self.code):
            # Try to detect and optimize multiplication patterns
            if self.detect_multiplication_pattern():
                continue

            inst = self.code[self.instruction_pointer].split()
            command = getattr(self, inst[0])
            command(*inst[1:])
        AoCUtils.print_solution(1, self.register["a"])


def main():
    """
    Main solution for Part 1: Run the assembunny code with register 'a' initialized to 7.
    The safe requires the final value in register 'a' after code execution.
    """
    # Initialize register 'a' to 7 as specified in Part 1
    initial_register_a = 7

    pc = BunnyPC()
    pc.register['a'] = initial_register_a
    pc.load(INPUT_FILE)
    pc.run()


if __name__ == "__main__":
    main()
