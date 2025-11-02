import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/3/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
from collections import defaultdict


def isTriangle(x, y, z):
    longest = max(x, y, z)
    other_two = sum([x, y, z]) - longest
    return longest < other_two


def main():

    lines = AoCInput.read_lines(INPUT_FILE)
    triangles = defaultdict(list)

    for idx, line in enumerate(lines):
        triangle_set = idx // 3
        for triangle_idx, side in enumerate(line.split()):
            triangles[(triangle_set, triangle_idx)].append(int(side))

    triangle_count = 0
    for sides in triangles.values():
        if isTriangle(*sides):
            triangle_count += 1

    AoCUtils.print_solution(2, triangle_count)


if __name__ == "__main__":
    main()
