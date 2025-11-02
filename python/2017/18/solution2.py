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
    def __init__(self, id):
        self.id = id
        self.duet = None
        self.program = []
        self.buffer = []
        self.tx_count = 0
        self.pointer = 0
        self.locked = False
        self.registers = defaultdict(int)

    def run(self):
        """executes the instructions and advances instruction pointer
        until out of range of instruction list"""
        while -1 < self.pointer < len(self.program):
            instruction = self.program[self.pointer]
            #print(f"pc{self.id} - {instruction}")
            i = getattr(self, instruction[0])
            i(*instruction[1:],)
            if instruction[0] != 'jgz':
                self.pointer += 1
            if self.locked == True:
                return
        self.locked = True
        return

    def snd(self, x):
        """send value to other program"""
        self.duet.buffer.append(str(self.get(x)))
        self.tx_count += 1

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
        """read value from buffer and write to X"""
        if len(self.buffer) > 0:
            self.locked = False
            self.registers[x] = self.get(self.buffer.pop(0))
            return
        else:
            self.locked = True
            self.pointer -= 1

    def jgz(self, x, y):
        """jumps with an offset of the value of Y,
        but only if the value of X is greater than zero.
        (An offset of 2 skips the next instruction, an
        offset of -1 jumps to the previous instruction, and so on.)"""

        if self.get(x) > 0:
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
    pc0.registers['p'] = 0
    pc1 = Duet(1)
    pc1.registers['p'] = 1

    pc0.duet = pc1
    pc1.duet = pc0

    lines = AoCInput.read_lines(INPUT_FILE)
    for line in lines:
        pc0.program.append(line.strip().split())
        pc1.program.append(line.strip().split())

    while pc0.locked == False or pc0.locked == False or len(pc0.buffer) > 0 or len(pc1.buffer) > 0:
        pc0.run()
        pc1.run()

    AoCUtils.print_solution(2, pc1.tx_count)


if __name__ == "__main__":
    main()
