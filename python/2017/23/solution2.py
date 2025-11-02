import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/23/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
from collections import defaultdict
from string import ascii_lowercase as letters
from sympy import isprime


class Duet():
    """simulated computer"""
    def __init__(self, id):
        self.id = id
        self.duet = None
        self.program = []
        self.buffer = []
        self.tx_count = 0
        self.mul_count = 0
        self.pointer = 0
        self.locked = False
        self.registers = defaultdict(int)

    def run(self):
        """executes the instructions and advances instruction pointer
        until out of range of instruction list"""
        while -1 < self.pointer < len(self.program):
            instruction = self.program[self.pointer]
            print(f"pc{self.id}:{self.pointer} - {instruction[0]} - {instruction[1]} ({self.get(instruction[1])}) - {instruction[2]} - ({self.get(instruction[2])})")
            i = getattr(self, instruction[0])
            i(*instruction[1:],)
            if instruction[0] != 'jnz':
                self.pointer += 1
            if self.locked == True:
                return
            print(f"register b, d, e: {self.registers['b']} {self.registers['d']} {self.registers['e']}")

        self.locked = True
        return


    def set(self, x, y):
        """sets register X to the value of Y"""
        self.registers[x] = self.get(y)

    def sub(self, x, y):
        """decreases register X by the value of Y"""
        self.registers[x] -= self.get(y)

    def mul(self, x, y):
        """sets register X to the result of multiplying
        the value contained in register X by the value of Y"""
        self.registers[x] *= self.get(y)
        self.mul_count += 1

    def jnz(self, x, y):
        """jumps with an offset of the value of Y,
        but only if the value of X is not zero.
        (An offset of 2 skips the next instruction, an
        offset of -1 jumps to the previous instruction, and so on.)"""

        if self.get(x) != 0:
            self.pointer += self.get(y)
        else:
            self.pointer += 1

    def get(self,x):
        if x in letters:
            return self.registers[x]
        else:
            return int(x)


def main():
    pc0 = Duet(0)
    pc0.registers['a'] = 1

    lines = AoCInput.read_lines(INPUT_FILE)

    for line in lines:
        pc0.program.append(line.strip().split())

    """while not pc0.locked:
        pc0.run()
    AoCUtils.print_solution(2, pc.registers['h'])
    """

    # painful debugging to figure out actual ask
    test_val = 106500
    composite_count = 0
    for x in range(1001):
        if not isprime(test_val):
            composite_count += 1
        test_val += 17

    # not 85, 916
    AoCUtils.print_solution(2, composite_count)

if __name__ == "__main__":
    main()
