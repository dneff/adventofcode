"""
Advent of Code 2017 - Day 15: Dueling Generators (Part 2)

Generators now have additional criteria before producing values for the judge:
- Generator A only produces values that are multiples of 4
- Generator B only produces values that are multiples of 8

The judge is now only willing to consider 5 million pairs (instead of 40 million).

Each generator continues producing values until it generates one that meets its criteria,
then hands that value to the judge.
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/15/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


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
    seed_a = 873

    factor_b = 48271
    seed_b = 583

    gen_a = create_generator(factor_a, seed_a)
    gen_b = create_generator(factor_b, seed_b)

    matches = 0
    num_pairs = 5000000

    for _ in range(num_pairs):
        # Get next value from generator A that's a multiple of 4
        value_a = next(gen_a)
        while value_a % 4 != 0:
            value_a = next(gen_a)

        # Get next value from generator B that's a multiple of 8
        value_b = next(gen_b)
        while value_b % 8 != 0:
            value_b = next(gen_b)

        # Compare lowest 16 bits
        if format(value_a, 'b')[-16:] == format(value_b, 'b')[-16:]:
            matches += 1

    AoCUtils.print_solution(2, matches)


if __name__ == "__main__":
    main()
