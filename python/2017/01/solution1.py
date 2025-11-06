"""
Advent of Code 2017 - Day 1: Inverse Captcha (Part 1)

Solve the captcha by finding the sum of all digits that match the immediately following digit
in a circular sequence. The sequence wraps around, so the last digit is compared with the first.

Examples:
    - 1122 produces 3 (1 + 2)
    - 1111 produces 4 (1 + 1 + 1 + 1)
    - 1234 produces 0 (no matches)
    - 91212129 produces 9 (only the final 9 matches the first)
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/1/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402


def calculate_captcha_sum(digits):
    """
    Calculate the sum of digits that match the next digit in the circular sequence.

    Args:
        digits: List of integers representing the captcha digits

    Returns:
        Sum of all digits that match their next neighbor (with wraparound)
    """
    captcha_sum = 0

    # Check each digit against the next one
    for i in range(len(digits) - 1):
        if digits[i] == digits[i + 1]:
            captcha_sum += digits[i]

    # Check wraparound: last digit against first digit
    if digits[0] == digits[-1]:
        captcha_sum += digits[0]

    return captcha_sum


def main():
    """Solve the Inverse Captcha puzzle."""
    line = AoCInput.read_lines(INPUT_FILE)[0]
    digits = [int(x) for x in line.strip()]

    captcha_sum = calculate_captcha_sum(digits)
    AoCUtils.print_solution(1, captcha_sum)


if __name__ == "__main__":
    main()
