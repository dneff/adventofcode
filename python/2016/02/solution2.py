import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/2/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402


class Keypad:

    def __init__(self):
        self.position = (0, 2)
        self.keys = {
            (2, 0): "1",
            (1, 1): "2",
            (2, 1): "3",
            (3, 1): "4",
            (0, 2): "5",
            (1, 2): "6",
            (2, 2): "7",
            (3, 2): "8",
            (4, 2): "9",
            (1, 3): "A",
            (2, 3): "B",
            (3, 3): "C",
            (2, 4): "D",
        }

    def move(self, direction):
        self.offsets = {"U": (0, -1), "R": (1, 0), "D": (0, 1), "L": (-1, 0)}
        delta = self.offsets[direction]
        new_position = tuple([x + y for x, y in zip(self.position, delta)])
        if new_position in self.keys:
            self.position = new_position

    def getPosition(self):
        return self.keys[self.position]

    def reset(self):
        self.position = (1, 1)


def main():
    lines = AoCInput.read_lines(INPUT_FILE)

    bathroom = Keypad()

    code = ""
    for sequence in lines:
        for direction in sequence.strip():
            bathroom.move(direction)

        code += bathroom.getPosition()

    AoCUtils.print_solution(2, code)


if __name__ == "__main__":
    main()
