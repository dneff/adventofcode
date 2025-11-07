"""
Advent of Code 2017 - Day 10: Knot Hash (Part 2)

Implement the full Knot Hash algorithm with these modifications from Part 1:
1. Convert input to ASCII byte values instead of parsing as numbers
2. Append magic suffix: [17, 31, 73, 47, 23]
3. Run 64 rounds (preserving position and skip size between rounds)
4. Create dense hash: XOR each block of 16 numbers from sparse hash
5. Convert dense hash to hexadecimal string (two digits per number)

Examples:
    Empty string "" = a2582a3a0e66e6e86e3812dcb672a272
    "AoC 2017" = 33efeb34ea91902bb2f59c9920caa6cd
    "1, 2, 3" = 3efbe78a8d82f29979031a4aa0b16a9d
    "1, 2, 4" = 63960835bcdc130f0b66d7ff4f6a5a8e
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/10/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402
from collections import deque  # noqa: E402


def compute_knot_hash(input_string):
    """
    Compute the full Knot Hash for a given input string.

    Args:
        input_string: String to hash

    Returns:
        Hexadecimal hash string (32 characters)
    """
    # Convert input to ASCII byte values
    lengths = [ord(c) for c in input_string.strip()]
    # Append magic suffix
    lengths.extend([17, 31, 73, 47, 23])

    # Initialize ring with numbers 0-255
    ring = deque(range(256))
    total_offset = 0
    skip_size = 0

    # Run 64 rounds
    for _ in range(64):
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

    # Rotate back to original reference frame (sparse hash)
    ring.rotate(total_offset)

    # Create dense hash by XORing blocks of 16
    dense_hash = []
    for block_start in range(0, 256, 16):
        block = list(ring)[block_start:block_start + 16]
        xor_value = 0
        for num in block:
            xor_value ^= num
        dense_hash.append(xor_value)

    # Convert to hexadecimal string (2 digits per number)
    hex_hash = ''.join([hex(x)[2:].zfill(2) for x in dense_hash])
    return hex_hash


def main():
    """Compute and print the Knot Hash."""
    line = AoCInput.read_lines(INPUT_FILE)[0]
    hash_result = compute_knot_hash(line)
    AoCUtils.print_solution(2, hash_result)


if __name__ == "__main__":
    main()
