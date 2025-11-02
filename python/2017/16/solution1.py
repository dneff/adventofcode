import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/16/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
from socket import INADDR_MAX_LOCAL_GROUP


class Computer():
    def __init__(self):
        self.progs = list('abcdefghijklmnop')
        self.instructions = []


    def run(self):
        for i in self.instructions:
            if i[0] == 's':
                x = int(i[1:])
                self.spin(x)
            elif i[0] == 'x':
                x,y = [int(x) for x in i[1:].split('/')]
                self.exchange(x,y)
            elif i[0] == 'p':
                x,y = [x for x in i[1:].split('/')]
                self.partner(x,y)

    def spin(self, a):
        self.progs = self.progs[-a:] + self.progs[:-a]

    def exchange(self, a, b):
        self.progs[a],self.progs[b] = self.progs[b],self.progs[a]

    def partner(self, a, b):
        idx_a = self.progs.index(a)
        idx_b = self.progs.index(b)
        self.progs[idx_a],self.progs[idx_b] = self.progs[idx_b], self.progs[idx_a]


def main():
    line = AoCInput.read_lines(INPUT_FILE)[0]
    instructions = line.strip().split(',')

    pc = Computer()
    pc.instructions = instructions
    pc.run()
    AoCUtils.print_solution(1, ''.join(pc.progs))

    

if __name__ == "__main__":
    main()