from collections import defaultdict
def AoCUtils.print_solution(2, x):
    print(f"The solution is {x}")
def main():
    nodes = defaultdict(list)
    max_x = 0
    max_y = 0

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/22/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils

    for line in f.readlines():
        node, size, used, available, usage_pct = line.strip().split()
        _, x, y = node.split('-')
        x, y = x[1:], y[1:]
        if len(y) == 1:
            y = '0' + y
        x, y = int(x),int(y)
        max_x, max_y = max(x, max_x), max(y, max_y)
        node_id = (x,y)
        nodes[node_id] = [int(size[:-1]), int(used[:-1]), int(available[:-1]), int(usage_pct[:-1])]

    print(f"x = 0 -> {max_x}")
    for row in range(max_y + 1):
        data = ''
        for column in range(max_x + 1):
            used = nodes[(column, row)][1]
            datum = '.'
            if used > 100:
                datum = '#'
            if used == 0:
                datum = '_'
            if (column, row) == (0, 0):
                datum = 'F'
            if (column, row) == (max_x, 0):
                datum = 'S'

            data += datum

        print(data)
        
    # solve by hand from here. The algo is to A* path
    # search to beginning of S, then move it along via
    # sliding tile logic to F
    AoCUtils.print_solution(2, 213)


if __name__ == "__main__":
    main()