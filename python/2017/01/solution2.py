"""
Advent of Code 2017 - Day 1: Inverse Captcha (Part 2)

Solve the captcha by finding the sum of all digits that match the digit halfway around
the circular sequence. For a sequence of length n, compare each digit with the digit at
position (i + n/2) % n.

Examples:
    - 1212 produces 6 (four digits each matching their opposite: 1 + 2 + 1 + 2)
    - 1221 produces 0 (no digit matches the one halfway around)
    - 123425 produces 4 (only 2 matches the one halfway around)
    - 123123 produces 12 (all six digits match their opposite)
    - 12131415 produces 4 (only 1 matches the one halfway around)
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/1/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402


def calculate_captcha_sum_halfway(digits):
    """
    Calculate the sum of digits that match the digit halfway around the circular sequence.

    Args:
        digits: List of integers representing the captcha digits

    Returns:
        Sum of all digits that match their opposite (halfway around the circle)
    """
    captcha_sum = 0
    half = len(digits) // 2

    for i, _ in enumerate(digits):
        # Compare with the digit halfway around the circular list
        opposite_index = (i + half) % len(digits)
        if digits[i] == digits[opposite_index]:
            captcha_sum += digits[i]

    return captcha_sum


def main():
    """Solve the Inverse Captcha puzzle with halfway-around comparison."""
    line = AoCInput.read_lines(INPUT_FILE)[0]
    digits = [int(x) for x in line.strip()]

    captcha_sum = calculate_captcha_sum_halfway(digits)
    AoCUtils.print_solution(2, captcha_sum)


if __name__ == "__main__":
    main()
