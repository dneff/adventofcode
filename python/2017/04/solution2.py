import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/4/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def main():
    lines = AoCInput.read_lines(INPUT_FILE)
    valid_count = 0
    for line in lines:
        words = [''.join(sorted(x)) for x in line.strip().split()]
        if len(words) == len(set(words)):
            valid_count += 1

    AoCUtils.print_solution(2, valid_count)


if __name__ == "__main__":
    main()
