"""
Advent of Code 2017 - Day 14: Disk Defragmentation (Part 1)

Use knot hashes to generate a 128x128 grid representation. For each row 0-127, compute
the knot hash of "{key}-{row}", convert to binary, and count the '1' bits (used squares).

Each knot hash produces 32 hexadecimal digits (128 bits total). Each hex digit converts
to 4 binary bits: 0='0000', 1='0001', ... f='1111'. A '1' bit indicates a used square.

Example: Using key "flqrgnkx":
    Row 0: knot_hash("flqrgnkx-0") = "d4f76bdcbf838f8416ccfa8bc6d1f9e6"
    Converting to binary and counting 1s across all 128 rows gives 8108 used squares.

This solution reuses the knot hash implementation from Day 10.
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/14/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
from collections import deque


def compute_knot_hash(input_string):
    """
    Compute the full Knot Hash for a given input string (from Day 10).

    Args:
        input_string: String to hash

    Returns:
        Hexadecimal hash string (32 characters)
    """
    # Convert input to ASCII byte values
    lengths = [ord(c) for c in input_string]
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

            # Rotate the ring
            rotation = (length + skip_size) % len(ring)
            ring.rotate(-rotation)

            total_offset += length + skip_size
            skip_size += 1

    # Rotate back to original reference frame
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


def hex_to_binary(hex_string):
    """
    Convert hexadecimal string to binary string.

    Args:
        hex_string: Hexadecimal string

    Returns:
        Binary string (4 bits per hex digit)
    """
    binary = ''
    for char in hex_string:
        integer = int(char, 16)
        binary += format(integer, '04b')
    return binary


def main():
    """Count total used squares in the 128x128 grid."""
    disk_key = 'oundnydw'
    total_used = 0

    # Generate 128 rows
    for row in range(128):
        row_key = f"{disk_key}-{row}"
        knot_hash = compute_knot_hash(row_key)
        binary = hex_to_binary(knot_hash)
        total_used += binary.count('1')

    AoCUtils.print_solution(1, total_used)


if __name__ == "__main__":
    main()
