import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/11/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


class GridMap():
    directions = {
        'n':  (0, -1, 1),
        'ne': (1, -1, 0),
        'se': (1, 0, -1),
        's': (0, 1, -1),
        'sw': (-1, 1, 0),
        'nw': (-1, 0, 1)
    }

    def __init__(self):
        self.loc = (0, 0, 0)

    def move(self, dir):
        diff = self.directions[dir]
        self.loc = (self.loc[0] + diff[0], self.loc[1] + diff[1], self.loc[2] + diff[2])

    def distance(self):
        distance = sum([abs(x) for x in list(self.loc)]) // 2
        return distance


def main():
    line = AoCInput.read_lines(INPUT_FILE)[0]
    map = GridMap()
    moves = line.strip().split(',')
    max_dist = 0
    for m in moves:
        map.move(m)
        max_dist = max(max_dist, map.distance())

    AoCUtils.print_solution(2, max_dist)


if __name__ == "__main__":
    main()
