import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/19/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def main():
    lines = AoCInput.read_lines(INPUT_FILE)

    tubes = {}
    for y, line in enumerate(lines):
        for x, point in enumerate([*line]):
            if point != ' ':
                tubes[(x, y)] = point

    directions = [(0, 1), (-1, 0), (0, -1), (1, 0)]
    next_dir = [('-'), ('|'), ('-'), ('|')]
    position = (1, 0)
    heading = 0

    markers = ''
    while position in tubes:
        if tubes[position] in ['|', '-']:
            pass
        elif tubes[position] == '+':
            new_path = next_dir[heading]
            # next position is either left or right of current heading
            left = (heading - 1) % 4
            left_x, left_y  = position[0] + directions[left][0], position[1] + directions[left][1]
            right = (heading + 1) % 4

            if (left_x, left_y) in tubes and tubes[(left_x, left_y)] == new_path:
                heading = left
            else:
                heading = right
        else:
            markers = markers + tubes[position]

        x, y = position[0] + directions[heading][0], position[1] + directions[heading][1]
        position = (x, y)

    AoCUtils.print_solution(1, markers)


if __name__ == "__main__":
    main()
