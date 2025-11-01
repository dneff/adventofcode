import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/6/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
from collections import defaultdict


class Lights:
    def __init__(self):
        self.grid = defaultdict(int)

    def on(self, start, end):
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.grid[(row, column)] = 1

    def off(self, start, end):
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.grid[(row, column)] = 0

    def toggle(self, start, end):
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.grid[(row, column)] = (self.grid[(row, column)] + 1) % 2

    def lit(self):
        return sum(self.grid.values())


def solve_part1():
    lines = AoCInput.read_lines(INPUT_FILE)

    display = Lights()

    for line in lines:
        line = line.strip()
        line = line.replace("turn on", "on").replace("turn off", "off").replace("through", "")
        action, start, end = line.split()
        start = tuple([int(x) for x in start.split(",")])
        end = tuple([int(x) for x in end.split(",")])

        getattr(display, action)(start, end)

    return display.lit()


answer = solve_part1()
AoCUtils.print_solution(1, answer)
