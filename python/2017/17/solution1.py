import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/17/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def main():
    ring = [0]
    cycle_size = 2018
    step_size = 328
    idx = 0
    for i in range(1, cycle_size):
        idx = (idx + step_size) % len(ring)
        ring.insert(idx + 1, i)
        idx += 1

    AoCUtils.print_solution(1, ring[idx+1])


if __name__ == "__main__":
    main()
