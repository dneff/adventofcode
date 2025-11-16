"""
Advent of Code 2019 - Day 22: Slam Shuffle

Part 2: Determine which card ends up in position 2020 after shuffling
a deck of 119,315,717,514,047 cards exactly 101,741,582,076,661 times.

This requires a mathematical approach using Linear Congruential Generator (LCG)
representation and modular exponentiation, as simulating the full deck or even
tracking a single position through all repetitions would be computationally infeasible.

Key insight: All shuffle operations can be represented as linear transformations
in modular arithmetic: position_new = (increment * position_old + offset) % deck_size

We represent the inverse of the shuffling process (finding which card ends up at
a given position, rather than where a given card ends up) and use the LCG formula
for composition to efficiently compute the result after many repetitions.
"""

import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "../../"))

from aoc_helpers import AoCInput, AoCUtils, MathUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, "../../../../aoc-data/2019/22/input")


def parse_instructions(lines):
    """
    Parse shuffle instructions from input lines into structured tuples.

    Args:
        lines: List of instruction strings from the puzzle input

    Returns:
        List of tuples in the format (operation_type, parameter):
        - ("new_stack", None) for reversing the deck
        - ("cut", n) for cutting n cards from top (or -n from bottom)
        - ("deal_increment", n) for dealing with increment n
    """
    instructions = []
    for line in lines:
        line = line.strip()
        if line == "deal into new stack":
            instructions.append(("new_stack", None))
        elif line.startswith("cut"):
            n = int(line.split(" ")[-1])
            instructions.append(("cut", n))
        elif line.startswith("deal with increment"):
            n = int(line.split(" ")[-1])
            instructions.append(("deal_increment", n))
    return instructions


def mod_inverse(a: int, m: int) -> int:
    """
    Compute the modular multiplicative inverse of a modulo m.

    Finds x such that (a * x) % m == 1, using the Extended Euclidean Algorithm.
    This is required for inverting the "deal with increment" operation.

    Args:
        a: The number to find the inverse of
        m: The modulus

    Returns:
        The modular inverse of a modulo m

    Note:
        This only works when gcd(a, m) == 1. In this problem, both deck_size
        and the increment values are chosen such that this condition holds.
    """
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1


if __name__ == "__main__":
    # Read and parse shuffle instructions
    lines = AoCInput.read_lines(INPUT_FILE)
    instructions = parse_instructions(lines)

    # Constants from the problem (both are prime numbers, which ensures modular inverse exists)
    deck_size = 119315717514047
    repetitions = 101741582076661

    # We want to find which card ends up at position 2020
    target_position = 2020

    # Convert all shuffle operations to a single Linear Congruential Generator (LCG)
    # In LCG form: new_position = (increment * old_position + offset) % deck_size
    #
    # We work with the INVERSE operations (finding which card ends up at a position,
    # rather than where a card ends up) because that's what Part 2 asks for.
    #
    # Inverse transformations:
    # - new_stack: position -> deck_size - 1 - position
    #              In LCG: increment *= -1, offset += increment
    # - cut n: position -> position - n
    #          In LCG: offset += increment * n
    # - deal_increment n: position -> position / n (modular division)
    #                     In LCG: increment *= mod_inverse(n)

    lcg_increment = 1
    lcg_offset = 0

    for instruction_type, parameter in instructions:
        if instruction_type == "new_stack":
            # Inverse of "deal into new stack"
            lcg_increment = (-lcg_increment) % deck_size
            lcg_offset = (lcg_offset + lcg_increment) % deck_size
        elif instruction_type == "cut":
            # Inverse of "cut n"
            lcg_offset = (lcg_offset + lcg_increment * parameter) % deck_size
        elif instruction_type == "deal_increment":
            # Inverse of "deal with increment n"
            inverse = mod_inverse(parameter, deck_size)
            lcg_increment = (lcg_increment * inverse) % deck_size

    # Now we have a single LCG that represents one full shuffle sequence
    # To apply it 'repetitions' times, we use the formula for LCG composition:
    #
    # After n repetitions:
    # - increment_n = increment^n (mod deck_size)
    # - offset_n = offset * (1 - increment^n) / (1 - increment) (mod deck_size)
    #
    # This is a geometric series: offset * (1 + increment + increment^2 + ... + increment^(n-1))

    # Calculate increment^repetitions using fast modular exponentiation
    increment_n = pow(lcg_increment, repetitions, deck_size)

    # Calculate the combined offset using the geometric series formula
    # offset_n = offset * (1 - increment^n) / (1 - increment)
    offset_n = lcg_offset * (1 - increment_n) * mod_inverse((1 - lcg_increment) % deck_size, deck_size)
    offset_n %= deck_size

    # Apply the combined LCG to find which card ends up at target_position
    final_card = (offset_n + target_position * increment_n) % deck_size

    AoCUtils.print_solution(2, final_card)
