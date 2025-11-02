import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/2/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def main():
    lines = AoCInput.read_lines(INPUT_FILE)
    row_div = []
    for row in lines:
        r = [int(x) for x in row.split()]
        r.sort(reverse=True)

        for i, x in enumerate(r):
            for y in r[i+1:]:
                if x % y == 0:
                    row_div.append(x//y)
    AoCUtils.print_solution(2, sum(row_div))


if __name__ == "__main__":
    main()
