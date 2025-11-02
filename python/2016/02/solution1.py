import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/2/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


class Keypad:
    def __init__(self):
        self.position = (1, 1)

    def move(self, direction):
        self.offsets = {"U": (0, -1), "R": (1, 0), "D": (0, 1), "L": (-1, 0)}
        delta = self.offsets[direction]
        new_position = tuple([x + y for x, y in zip(self.position, delta)])
        if max(new_position) <= 2 and min(new_position) >= 0:
            self.position = new_position

    def getPosition(self):
        return self.position[0] + 1 + self.position[1] * 3

    def reset(self):
        self.position = (1, 1)


def main():
    lines = AoCInput.read_lines(INPUT_FILE)

    bathroom = Keypad()

    code = []
    for sequence in lines:
        for direction in sequence.strip():
            bathroom.move(direction)


        code.append(bathroom.getPosition())

    code = ''.join([str(x) for x in code])
    AoCUtils.print_solution(1, code)


if __name__ == "__main__":
    main()