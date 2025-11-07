"""
Advent of Code 2017 - Day 15: Dueling Generators (Part 2)

Generators now have additional criteria before producing values for the judge:
- Generator A only produces values that are multiples of 4
- Generator B only produces values that are multiples of 8

The judge is now only willing to consider 5 million pairs (instead of 40 million).

Each generator continues producing values until it generates one that meets its criteria,
then hands that value to the judge.

Optimizations:
- Use bitwise AND for divisibility: (value & 3) for mod 4, (value & 7) for mod 8
- Use bitwise AND (value & 0xFFFF) to extract lowest 16 bits
- Compute values inline to avoid generator function call overhead

Performance: ~9s (down from 12s with original approach)
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
    """Count matches in the lowest 16 bits over 5 million filtered pairs."""
    # Input values for the generators
    factor_a = 16807
    value_a = 873

    factor_b = 48271
    value_b = 583

    matches = 0
    num_pairs = 5000000
    modulo = 2147483647

    for _ in range(num_pairs):
        # Get next value from generator A that's a multiple of 4
        # Using bitwise AND: value & 3 == 0 is equivalent to value % 4 == 0
        value_a = (value_a * factor_a) % modulo
        while value_a & 3:
            value_a = (value_a * factor_a) % modulo

        # Get next value from generator B that's a multiple of 8
        # Using bitwise AND: value & 7 == 0 is equivalent to value % 8 == 0
        value_b = (value_b * factor_b) % modulo
        while value_b & 7:
            value_b = (value_b * factor_b) % modulo

        # Compare lowest 16 bits using bitwise AND
        if (value_a & 0xFFFF) == (value_b & 0xFFFF):
            matches += 1

    AoCUtils.print_solution(2, matches)


if __name__ == "__main__":
    main()
