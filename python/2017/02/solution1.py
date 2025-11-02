import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/2/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def main():
    lines = AoCInput.read_lines(INPUT_FILE)
    row_minmax = []
    for row in lines:
        r = [int(x) for x in row.split()]
        row_minmax.append(max(r) - min(r))

    AoCUtils.print_solution(1, sum(row_minmax))


if __name__ == "__main__":
    main()
