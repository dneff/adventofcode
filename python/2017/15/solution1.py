"""
Advent of Code 2017 - Day 15: Dueling Generators (Part 1)

Two generators produce values using modular arithmetic. A judge compares the lowest 16 bits
of each generator's output and counts matches. Count the number of matches in 40 million pairs.

Generator A: multiplies previous value by 16807, then modulo 2147483647
Generator B: multiplies previous value by 48271, then modulo 2147483647

The judge compares the lowest 16 bits of each value. Match detection can be done by:
- Converting to binary and comparing last 16 characters
- Or using modulo 65536 (2^16) to get lowest 16 bits as integer

Example (starting values 65, 8921):
    After 40 million pairs, 588 matches are found.
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
    """Count matches in the lowest 16 bits over 40 million pairs."""
    # Input values for the generators
    factor_a = 16807
    seed_a = 873

    factor_b = 48271
    seed_b = 583

    gen_a = create_generator(factor_a, seed_a)
    gen_b = create_generator(factor_b, seed_b)

    matches = 0
    num_pairs = 40000000

    for _ in range(num_pairs):
        # Get next values and convert lowest 16 bits to binary
        value_a = format(next(gen_a), 'b')[-16:]
        value_b = format(next(gen_b), 'b')[-16:]

        if value_a == value_b:
            matches += 1

    AoCUtils.print_solution(1, matches)


if __name__ == "__main__":
    main()
