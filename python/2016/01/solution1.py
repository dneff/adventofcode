import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/1/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402


class GridBug:

    def __init__(self):
        self.directions = ["N", "E", "S", "W"]
        self.location = (0, 0)
        self.orientation = 0
        self.offsets = {"N": (0, 1), "E": (1, 0), "S": (0, -1), "W": (-1, 0)}

    def turn(self, direction):
        if direction == "L":
            self.orientation = (self.orientation - 1) % 4
        elif direction == "R":
            self.orientation = (self.orientation + 1) % 4

    def move(self, distance):
        direction = self.directions[self.orientation]
        for _ in range(distance):
            self.location = tuple([x + y for x, y in zip(self.location, self.offsets[direction])])

    def getDistance(self):
        return abs(self.location[0]) + abs(self.location[1])


def main():
    lines = AoCInput.read_lines(INPUT_FILE)

    sleigh = GridBug()

    instructions = [(x[0], int(x[1:])) for x in lines[0].split(", ")]
    for i in instructions:
        sleigh.turn(i[0])
        sleigh.move(i[1])

    AoCUtils.print_solution(1, sleigh.getDistance())


if __name__ == "__main__":
    main()
