"""
Advent of Code 2017 - Day 15: Dueling Generators (Part 1)

Two generators produce values using modular arithmetic. A judge compares the lowest 16 bits
of each generator's output and counts matches. Count the number of matches in 40 million pairs.

Generator A: multiplies previous value by 16807, then modulo 2147483647
Generator B: multiplies previous value by 48271, then modulo 2147483647

The judge compares the lowest 16 bits of each value. Optimized approach:
- Use bitwise AND (value & 0xFFFF) to extract lowest 16 bits (much faster than binary strings)
- Compute values inline to avoid generator function call overhead

Example (starting values 65, 8921):
    After 40 million pairs, 588 matches are found.

Performance: ~12s (down from 27s with original string-based approach)
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/15/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCUtils  # noqa: E402


def create_generator(factor, initial_value):
    """
    Create a generator that produces values using modular arithmetic.

    Args:
        factor: Multiplication factor for the generator
        initial_value: Starting value (seed)

    Yields:
        Next generated value
    """
    value = initial_value
    while True:
        value = (value * factor) % 2147483647
        yield value


def main():
    """Count matches in the lowest 16 bits over 40 million pairs."""
    # Input values for the generators
    factor_a = 16807
    value_a = 873

    factor_b = 48271
    value_b = 583

    matches = 0
    num_pairs = 40000000
    modulo = 2147483647

    for _ in range(num_pairs):
        # Generate next values inline (eliminates generator function call overhead)
        value_a = (value_a * factor_a) % modulo
        value_b = (value_b * factor_b) % modulo

        # Compare lowest 16 bits using bitwise AND
        if (value_a & 0xFFFF) == (value_b & 0xFFFF):
            matches += 1

    AoCUtils.print_solution(1, matches)


if __name__ == "__main__":
    main()
