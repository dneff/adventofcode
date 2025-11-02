import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/14/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
from collections import deque


def knot_hash(s):
    """generate knothash from string"""
    instructions = [ord(x) for x in s]
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

    return ''.join([hex(x)[2:] for x in hashes])


def hash_to_binary(h):
    result = ''
    for c in h:
        integer = int(c, 16)
        result = result + format(integer,'0>4b')
    return result


def main():
    used = 0
    input = 'oundnydw'
    for r in range(128):
        row_hash = f"{input}-{r}"
        k = knot_hash(row_hash)
        used += hash_to_binary(k).count('1')
    AoCUtils.print_solution(1, used)


if __name__ == "__main__":
    main()