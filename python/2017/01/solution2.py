import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/1/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def main():
    """ calculate solution """
    line = AoCInput.read_lines(INPUT_FILE)[0]
    digits = [int(x) for x in line.strip()]

    same_sum = 0
    half = len(digits)//2
    for i, _ in enumerate(digits):
        # if digit halfway around matches,the add to same_sum
        compare = (i + half) % len(digits)
        if digits[i] == digits[compare]:
            same_sum += digits[i]
    AoCUtils.print_solution(2, same_sum)


if __name__ == "__main__":
    main()
