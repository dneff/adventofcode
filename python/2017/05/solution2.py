import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/5/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def main():
    lines = AoCInput.read_lines(INPUT_FILE)
    instructions = [int(value) for value in lines]

    step = 0
    offset = 0
    while 0 <= offset <= (len(instructions) - 1):
        step += 1
        delta = instructions[offset]
        if delta >= 3:
            instructions[offset] -= 1
        else:
            instructions[offset] += 1
        offset += delta

    AoCUtils.print_solution(2, step)


if __name__ == "__main__":
    main()
