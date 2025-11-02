import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/17/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def main():
    ring = 1
    cycle_size = 50000000
    step_size = 328
    idx = 0
    result = 0
    for i in range(1, cycle_size):
        idx = (idx + step_size) % ring
        ring += 1
        idx += 1
        if idx == 1:
            result = i
    AoCUtils.print_solution(2, result)


if __name__ == "__main__":
    main()
