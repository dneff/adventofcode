import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/6/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402
from collections import defaultdict  # noqa: E402
from operator import itemgetter  # noqa: E402


def getMaxKey(dict_x):
    ordered_keys = [x for x, y in sorted(dict_x.items(), key=itemgetter(1), reverse=True)]
    return ordered_keys[0]


def main():
    lines = AoCInput.read_lines(INPUT_FILE)

    position = []

    for _ in range(8):
        position.append(defaultdict(int))

    for line in lines:
        for index, char in enumerate(line.strip()):
            position[index][char] += 1

    message = ""
    for d in position:
        message += getMaxKey(d)

    AoCUtils.print_solution(1, message)


if __name__ == "__main__":
    main()
