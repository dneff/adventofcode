"""
Advent of Code 2017 - Day 14: Disk Defragmentation (Part 2)

Count the number of contiguous regions in the 128x128 grid. A region is a group of used
squares (1s) that are connected horizontally or vertically (not diagonally).

Generate the grid using knot hashes (same as Part 1), then use graph algorithms to find
connected components. The solution uses NetworkX to create a 2D lattice graph, removes
unused nodes (0s), and counts the strongly connected components.
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/14/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
from collections import deque
import networkx as nx


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

    # Convert to hexadecimal string with proper zero-padding
    hex_hash = ''.join([format(x, '02x') for x in dense_hash])
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
    """Count the number of contiguous regions in the grid."""
    disk_key = 'oundnydw'

    # Create a 128x128 grid graph with all nodes initially connected
    grid = nx.generators.lattice.grid_2d_graph(128, 128)

    # Generate the disk representation and remove unused squares
    for row in range(128):
        row_key = f"{disk_key}-{row}"
        knot_hash = compute_knot_hash(row_key)
        binary = hex_to_binary(knot_hash)

        # Remove nodes where the bit is '0' (unused)
        for col, bit in enumerate(binary):
            if bit == '0':
                grid.remove_node((col, row))

    # Convert to directed graph and find connected components
    grid = nx.to_directed(grid)
    condensed = nx.condensation(grid)

    # Count the number of unique components
    num_regions = len(set(condensed.graph['mapping'].values()))

    AoCUtils.print_solution(2, num_regions)


if __name__ == "__main__":
    main()
