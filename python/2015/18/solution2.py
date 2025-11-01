import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/18/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
from collections import defaultdict


class Display:
    def __init__(self):
        self.lights = {}
        self.step = 0
        self.width = 0

    def add(self, light):
        self.lights[light] = True

    def getNeighbors(self, point):
        neighbors = []
        offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for offset in offsets:
            possible = tuple(map(sum, zip(point, offset)))
            if max((possible)) > self.width or min(possible) < 0:
                continue
            neighbors.append(possible)
        return neighbors

    def lightCorners(self):
        corners = [(0, 0), (0, self.width), (self.width, 0), (self.width, self.width)]
        for light in corners:
            self.lights[light] = True

    def cycle(self):
        on = []
        neighbors = defaultdict(int)
        for light in self.lights:
            for neighbor in self.getNeighbors(light):
                neighbors[neighbor] += 1
        off = [k for k in self.lights if neighbors[k] not in [2, 3]]
        on = [k for k, v in neighbors.items() if v == 3]
        for light in off:
            self.lights.pop(light)
        for light in on:
            self.lights[light] = True
        self.lightCorners()
        self.step += 1

    def display(self):
        grid = []
        for r in range(self.width + 1):
            row = ""
            for c in range(self.width + 1):
                if (r, c) in self.lights:
                    row = row + "#"
                else:
                    row = row + "."
            grid.append(row)
        return ('\n').join(grid)


def solve_part2():
    lines = AoCInput.read_lines(INPUT_FILE)

    step_count = 100
    xmas_lights = Display()

    width = 0
    for row, line in enumerate(lines):
        for column, char in enumerate(line.strip()):
            if char == "#":
                xmas_lights.add((row, column))
        width = max(width, row)

    xmas_lights.width = width
    xmas_lights.lightCorners()

    while xmas_lights.step < step_count:
        xmas_lights.cycle()

    return len(xmas_lights.lights)


answer = solve_part2()
AoCUtils.print_solution(2, answer)
