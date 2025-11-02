import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/10/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
from collections import deque


def main():
    """main solution for problem"""
    line = AoCInput.read_lines(INPUT_FILE)[0]
    instructions = [int(x) for x in line.strip().split(',')]
    offset = 0
    skip_size = 0
    ring = deque()
    ring.extend(range(256))

    for i in instructions:
        flip, keep = list(ring)[:i], list(ring)[i:]
        flip.reverse()
        ring = deque(flip + keep)

        ring.rotate(-((i + skip_size) % len(ring)))

        offset += i + skip_size
        skip_size += 1

    ring.rotate(offset)
    AoCUtils.print_solution(1, ring[0] * ring[1])


if __name__ == "__main__":
    main()
