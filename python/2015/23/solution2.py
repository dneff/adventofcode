import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/23/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


class Computer:
    def __init__(self):
        self.index = 0
        self.registers = {"a": 0, "b": 0}
        self.instructions = []

    def load(self, data):
        for line in data:
            self.instructions.append(line.strip().split())

    def run(self):
        while self.index < len(self.instructions):
            inst = self.instructions[self.index]
            command = getattr(self, inst[0])
            if len(inst) == 2:
                command(inst[-1])
            else:
                command(inst[1][0], inst[-1])

    def hlf(self, r):
        self.registers[r] = self.registers[r] // 2
        self.index += 1

    def tpl(self, r):
        self.registers[r] *= 3
        self.index += 1

    def inc(self, r):
        self.registers[r] += 1
        self.index += 1

    def jmp(self, offset):
        self.index += int(offset)

    def jie(self, r, offset):
        if self.registers[r] % 2 == 0:
            self.index += int(offset)
        else:
            self.index += 1

    def jio(self, r, offset):
        if self.registers[r] == 1:
            self.index += int(offset)
        else:
            self.index += 1


def solve_part2():

    gift = Computer()

    lines = AoCInput.read_lines(INPUT_FILE)
    gift.load(lines)

    gift.registers['a'] = 1
    gift.run()

    return gift.registers['b']

answer = solve_part2()
AoCUtils.print_solution(2, answer)
