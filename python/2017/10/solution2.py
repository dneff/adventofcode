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
    instructions = [ord(x) for x in line.strip()]
    instructions.extend([17, 31, 73, 47, 23])

    ring = deque()
    ring.extend(range(256))
    offset = 0
    skip_size = 0
    for _ in range(64):

        for i in instructions:
            flip, keep = list(ring)[:i], list(ring)[i:]
            flip.reverse()
            ring = deque(flip + keep)
            ring.rotate(-((i + skip_size) % len(ring)))
            offset += i + skip_size
            skip_size += 1

    ring.rotate(offset)

    hashes = []
    for block in range(0, 256, 16):
        hash_val = 0
        for x in list(ring)[block:block+16]:
            hash_val ^= x
        hashes.append(hash_val)

    AoCUtils.print_solution(2, ''.join([hex(x)[2:] for x in hashes]))


if __name__ == "__main__":
    main()
