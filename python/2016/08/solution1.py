import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/8/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402


class cardReader():

    def __init__(self):
        self.height = 6
        self.width = 50
        self.screen = []
        for _ in range(self.height):
            row = ['.'] * self.width
            self.screen.append(row)

    def rect(self, w, h):
        for row in range(h):
            for col in range(w):
                self.screen[row][col] = '#'

    def rotateColumn(self, column, count):
        col = {}
        for row in range(self.height):
            col[row] = self.screen[row][column]
        for row in range(self.height):
            new_value = col[(row - count) % self.height]
            self.screen[row][column] = new_value

    def rotateRow(self, row, count):
        count = count % self.width
        self.screen[row] = self.screen[row][-count:] + \
            self.screen[row][:-count]

    def litCount(self):
        return sum([row.count('#') for row in self.screen])


def main():

    door = cardReader()

    lines = AoCInput.read_lines(INPUT_FILE)
    for line in lines:
        line = line.strip()
        line = line.replace('x=', '')
        line = line.replace('y=', '')
        line = line.replace('by', '')
        line = line.replace('x', ' ')
        line = line.replace('rotate column', 'rotateColumn')
        line = line.replace('rotate row', 'rotateRow')
        line = line.split()

        instruction = getattr(door, line[0])
        instruction(int(line[1]), int(line[2]))

    AoCUtils.print_solution(1, door.litCount())


if __name__ == '__main__':
    main()
