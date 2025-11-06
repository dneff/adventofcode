"""
Advent of Code 2017 - Day 10: Knot Hash (Part 1)

Implement a hash function that simulates knot-tying on a circular list of 256 numbers
(0-255). Process a sequence of input lengths, and for each length:
1. Reverse that many elements starting at the current position
2. Move current position forward by (length + skip size)
3. Increment skip size by 1

The list wraps around circularly. After processing all lengths, multiply the first two
numbers in the list.

Example (with 5-element list and lengths [3, 4, 1, 5]):
    Start: [0, 1, 2, 3, 4], pos=0, skip=0
    After length 3: [2, 1, 0, 3, 4], pos=3, skip=1
    After length 4: [4, 3, 0, 1, 2], pos=3, skip=2
    After length 1: [4, 3, 0, 1, 2], pos=1, skip=3
    After length 5: [3, 4, 2, 1, 0], pos=4, skip=4
    Result: 3 * 4 = 12
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/10/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402
from collections import deque  # noqa: E402


def process_knot_hash(ring, lengths):
    """
    Process the knot hash algorithm on a circular ring.

    Args:
        ring: Deque representing the circular list of numbers
        lengths: List of reversal lengths to process

    Returns:
        Tuple of (final_ring, total_offset) after processing
    """
    total_offset = 0
    skip_size = 0

    for length in lengths:
        # Reverse the first 'length' elements
        reversed_section = list(ring)[:length]
        reversed_section.reverse()
        remaining_section = list(ring)[length:]
        ring = deque(reversed_section + remaining_section)

        # Rotate the ring by (length + skip_size)
        rotation = (length + skip_size) % len(ring)
        ring.rotate(-rotation)

        total_offset += length + skip_size
        skip_size += 1

    return ring, total_offset


def main():
    """Process knot hash and calculate product of first two numbers."""
    line = AoCInput.read_lines(INPUT_FILE)[0]
    lengths = [int(x) for x in line.strip().split(',')]

    # Initialize ring with numbers 0-255
    ring = deque(range(256))

    ring, total_offset = process_knot_hash(ring, lengths)

    # Rotate back to original reference frame
    ring.rotate(total_offset)

    # Multiply first two numbers
    result = ring[0] * ring[1]
    AoCUtils.print_solution(1, result)


if __name__ == "__main__":
    main()
