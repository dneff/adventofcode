"""
Advent of Code 2018 - Day 19: Go With The Flow
https://adventofcode.com/2018/day/19

This puzzle involves understanding how an instruction pointer can be bound to a register,
enabling flow control in a device's programming language. The solution executes a program
with six registers where the instruction pointer's value is written to a bound register
before each instruction and read back after execution.
"""
import os
import sys
import copy

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2018/19/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))
from aoc_helpers import AoCUtils


class WristCalc:
    """Simulates a device with 6 registers, instruction pointer binding, and 16 opcodes."""

    def __init__(self):
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

    def reset(self):
        self.registers = [0] * len(self.registers)

    def run(self):
        """Execute the program until the instruction pointer goes out of bounds."""
        while 0 <= self.pointer < len(self.instructions):
            # Write pointer value to bound register
            self.registers[self.pointer_register] = self.pointer
            # Execute current instruction
            inst, a, b, c = self.instructions[self.pointer]
            self.commands[inst](a, b, c)
            # Read back pointer from bound register and advance
            self.pointer = self.registers[self.pointer_register]
            self.pointer += 1
            # Debug output
            print(f"{self.registers[0]}\t{self.registers[1]}\t{self.registers[2]}\t"
                  f"{self.registers[3]}\t{self.registers[4]}\t{self.registers[5]}\t")

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
    """Load and execute the program, returning the value in register 0."""
    file = open(INPUT_FILE, 'r', encoding='utf-8')
    calc = WristCalc()

    # Load instruction pointer binding from first line
    calc.pointer_register = int(file.readline().strip().split()[1])

    # Load program instructions
    for line in file.readlines():
        data = line.strip().split()
        args = [int(x) for x in data[1:]]
        command = data[0]
        calc.instructions.append([command] + args)

    # Set register 0 to 1 as specified in the problem
    calc.registers[0] = 1
    calc.run()
    AoCUtils.print_solution(1, calc.registers[0])


if __name__ == "__main__":
    main()
