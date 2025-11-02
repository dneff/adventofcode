import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/18/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
from collections import defaultdict
from string import ascii_lowercase as letters


class Duet():
    """simulated computer"""
    def __init__(self):
        self.program = []
        self.played = 0
        self.pointer = 0
        self.registers = defaultdict(int)

    def run(self):
        """executes the instructions and advances instruction pointer
        until out of range of instruction list"""
        while -1 < self.pointer < len(self.program):
            instruction = self.program[self.pointer]
            i = getattr(self, instruction[0])
            i(*instruction[1:],)
            if instruction[0] != 'jgz':
                self.pointer += 1

    def snd(self, x):
        """plays a sound with a frequency equal to the value of X"""
        self.played = self.registers[x]

    def set(self, x, y):
        """sets register X to the value of Y"""
        self.registers[x] = self.get(y)

    def add(self, x, y):
        """increases register X by the value of Y"""
        self.registers[x] += self.get(y)

    def mul(self, x, y):
        """sets register X to the result of multiplying
        the value contained in register X by the value of Y"""
        self.registers[x] *= self.get(y)

    def mod(self, x, y):
        """sets register X to the remainder of dividing
        the value contained in register X by the value
        of Y (that is, it sets X to the result of X modulo Y)"""
        self.registers[x] %= self.get(y)

    def rcv(self, x):
        """recovers the frequency of the last sound
        played, but only when the value of X is not zero.
        (If it is zero, the command does nothing.)"""
        if self.registers[x] != 0:
            self.registers[x] = self.played
            if self.played != 0:
                AoCUtils.print_solution(1, self.played)
                exit(0)

    def jgz(self, x, y):
        """jumps with an offset of the value of Y,
        but only if the value of X is greater than zero.
        (An offset of 2 skips the next instruction, an
        offset of -1 jumps to the previous instruction, and so on.)"""
        if self.get(x) > 0:
            self.pointer += self.get(y)
        else:
            self.pointer += 1

    def get(self, x):
        if x in letters:
            return self.registers[x]
        else:
            return int(x)


def main():
    pc = Duet()
    lines = AoCInput.read_lines(INPUT_FILE)
    for line in lines:
        pc.program.append(line.strip().split())

    pc.run()


if __name__ == "__main__":
    main()
