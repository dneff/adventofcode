"""
Advent of Code 2018 - Day 21: Chronal Conversion (Part 1)
https://adventofcode.com/2018/day/21

The puzzle involves a time travel device with an activation system program that needs
to halt to enable an integer underflow. We need to find the value for register 0 that
causes the program to halt after executing the fewest instructions.

The program computes a sequence of values in register 5 (r5) using a hash-like algorithm,
and at instruction 28 checks if r5 == r0. If they match, the program halts.

Approach:
- Run the program with r0=0 and break when instruction pointer reaches 28
- The value in r5 at that point is the first value the program checks against r0
- Setting r0 to this value causes the program to halt on the very first check (~1845 instructions)
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2018/21/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils

class WristCalc:
    """Simulates a device with 6 registers, instruction pointer binding, and 16 opcodes."""

    def __init__(self):
        self.cycles = 0
        self.registers = [0] * 6
        self.instructions = []
        self.commands = {}
        self.pointer = 0  # Instruction pointer
        self.pointer_register = 0  # Which register the pointer is bound to
        self.command_names = [
            'addr', 'addi', 'mulr', 'muli',
            'banr', 'bani', 'borr', 'bori',
            'setr', 'seti',
            'gtri', 'gtir', 'gtrr',
            'eqri', 'eqir', 'eqrr'
        ]
        # Map command names to their functions
        for command in self.command_names:
            func = getattr(self, command)
            self.commands[command] = func

    def setRegisters(self, values):
        for i, x in enumerate(values):
            self.registers[i] = x

    def getRegisters(self):
        return self.registers

    def reset(self, max_steps=-1):
        self.max_steps = max_steps
        self.registers = [0] * len(self.registers)

    def run(self, max_steps=-1):
        """ Execute the program until the instruction pointer goes out of bounds,
            max_steps is reached, or pointer reaches instruction 28 (halt check).
            If max_steps is -1, run until completion or instruction 28.
        """
        if max_steps > 0:
            self.cycles = 0
        while 0 <= self.pointer < len(self.instructions):
            # Write pointer value to bound register
            self.registers[self.pointer_register] = self.pointer
            # Execute current instruction
            inst, a, b, c = self.instructions[self.pointer]
            self.commands[inst](a, b, c)
            # Read back pointer from bound register and advance
            self.pointer = self.registers[self.pointer_register]
            self.pointer += 1

            # Debug output (uncomment to trace execution)
            # print(f"{self.registers[0]}\t{self.registers[1]}\t{self.registers[2]}\t"
            #       f"{self.registers[3]}\t{self.registers[4]}\t{self.registers[5]}\t"
            #       f"ip={self.pointer}\tcycle={self.cycles}\t\tinst={inst} {a} {b} {c}")

            if max_steps > 0:
                self.cycles += 1
                if self.cycles >= max_steps or self.pointer == 28:
                    break

    def addr(self, a, b, c):
        # (add register) stores into register C
        # the result of adding register A and register B.
        self.registers[c] = self.registers[a] + self.registers[b]

    def addi(self, a, b, c):
        # (add immediate) stores into register C
        # the result of adding register A and value B.
        self.registers[c] = self.registers[a] + b

    def mulr(self, a, b, c):
        # (multiply register) stores into register C
        # the result of multiplying register A
        # and register B.
        self.registers[c] = self.registers[a] * self.registers[b]

    def muli(self, a, b, c):
        # (multiply immediate) stores into
        # register C the result of multiplying
        # register A and value B.
        self.registers[c] = self.registers[a] * b

    def banr(self, a, b, c):
        # (bitwise AND register) stores into
        # register C the result of the bitwise
        # AND of register A and register B.
        self.registers[c] = self.registers[a] & self.registers[b]

    def bani(self, a, b, c):
        # (bitwise AND immediate) stores into
        # register C the result of the bitwise AND
        # of register A and value B.
        self.registers[c] = self.registers[a] & b

    def borr(self, a, b, c):
        # (bitwise OR register) stores into
        # register C the result of the bitwise OR
        # of register A and register B.
        self.registers[c] = self.registers[a] | self.registers[b]

    def bori(self, a, b, c):
        # (bitwise OR immediate) stores into
        # register C the result of the bitwise OR
        # of register A and value B.
        self.registers[c] = self.registers[a] | b

    def setr(self, a, b, c):
        # (set register) copies the contents of
        # register A into register C.
        # (Input B is ignored.)
        self.registers[c] = self.registers[a]

    def seti(self, a, b, c):
        # (set immediate) stores value A
        # into register C. (Input B is ignored.)
        self.registers[c] = a

    def gtir(self, a, b, c):
        # (greater-than immediate/register) sets
        # register C to 1 if value A is greater
        # than register B. Otherwise, register C is set to 0.
        if a > self.registers[b]:
            self.registers[c] = 1
        else:
            self.registers[c] = 0

    def gtri(self, a, b, c):
        # (greater-than register/immediate) sets
        # register C to 1 if register A is greater
        # than value B. Otherwise, register C is set to 0.
        if self.registers[a] > b:
            self.registers[c] = 1
        else:
            self.registers[c] = 0

    def gtrr(self, a, b, c):
        # (greater-than register/register) sets
        # register C to 1 if register A is greater
        # than register B. Otherwise, register C is set to 0.
        if self.registers[a] > self.registers[b]:
            self.registers[c] = 1
        else:
            self.registers[c] = 0

    def eqir(self, a, b, c):
        # (equal immediate/register) sets register C
        # to 1 if value A is equal to register B.
        # Otherwise, register C is set to 0.
        if a == self.registers[b]:
            self.registers[c] = 1
        else:
            self.registers[c] = 0

    def eqri(self, a, b, c):
        # (equal register/immediate) sets register C
        # to 1 if register A is equal to value B.
        # Otherwise, register C is set to 0.
        if self.registers[a] == b:
            self.registers[c] = 1
        else:
            self.registers[c] = 0

    def eqrr(self, a, b, c):
        # (equal register/register) sets register C
        # to 1 if register A is equal to register B.
        # Otherwise, register C is set to 0.
        if self.registers[a] == self.registers[b]:
            self.registers[c] = 1
        else:
            self.registers[c] = 0

def main():
    file = AoCInput.read_lines(INPUT_FILE)
    calc = WristCalc()

    # Load instruction pointer binding from first line
    calc.pointer_register = int(file[0].strip().split()[1])

    # Load program instructions
    for line in file[1:]:
        data = line.strip().split()
        args = [int(x) for x in data[1:]]
        command = data[0]
        calc.instructions.append([command] + args)

    # Run the program with r0=0 and break when we reach instruction 28 (the halt check)
    # At instruction 28, the program checks if r5 == r0
    # The WristCalc.run() method breaks when pointer == 28 (see line 75)
    calc.setRegisters([0, 0, 0, 0, 0, 0])
    calc.run(max_steps=100000)

    # The value in r5 is the first value checked against r0
    # This is the optimal answer - causes halt in fewest instructions
    answer = calc.registers[5]

    AoCUtils.print_solution(1, answer)

if __name__ == '__main__':
    main()
