import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/8/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
from collections import defaultdict
from dis import Instruction


class Computer():
    def __init__(self):
        self.instructions = []
        self.register = defaultdict(int)
        self.max_mem = 0

    def run(self):
        for i in self.instructions:
            inst = 'self.register[\'' + i[0] + '\']'
            if i[1] == 'inc':
                inst = f"{inst} += {i[2]}"
            else:
                inst = f"{inst} -= {i[2]}"
            cond = f"self.register['{i[4]}'] {i[5]} {i[6]}"

            if eval(cond):
                exec(inst)
                self.max_mem = max(self.max_mem, max(self.register.values()))


def main():
    pc = Computer()
    lines = AoCInput.read_lines(INPUT_FILE)
    for line in lines:
        pc.instructions.append(line.strip().split())

    pc.run()

    AoCUtils.print_solution(2, pc.max_mem)


if __name__ == "__main__":
    main()