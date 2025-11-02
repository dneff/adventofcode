import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/1/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def main():
    """ calculates solution """
    line = AoCInput.read_lines(INPUT_FILE)[0]
    digits = [int(x) for x in line.strip()]

    same_sum = 0
    for i in range(len(digits) - 1):
        # if the next digit matches,the add to same_sum
        if digits[i] == digits[i + 1]:
            same_sum += digits[i]
    if digits[0] == digits[-1]:
        same_sum += digits[0]
    AoCUtils.print_solution(1, same_sum)


if __name__ == "__main__":
    main()
