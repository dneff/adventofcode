"""
Advent of Code 2019 - Day 4: Secure Container
Part 1: Count valid passwords within a range.

The password is a six-digit number that meets these criteria:
- Two adjacent digits are the same (like 22 in 122345)
- Going from left to right, digits never decrease (only increase or stay the same)
- The value is within the puzzle input range

Examples:
- 111111 is valid (has adjacent matching digits, never decreases)
- 223450 is invalid (digits decrease: 5 to 0)
- 123789 is invalid (no adjacent matching digits)
"""
import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCUtils  # noqa: E402


def has_adjacent_matching_digits(number):
    """
    Check if the number has at least two adjacent matching digits.

    Args:
        number: A six-digit number

    Returns:
        True if any two adjacent digits are the same
    """
    digits = str(number)
    for i in range(len(digits) - 1):
        if digits[i] == digits[i + 1]:
            return True
    return False


def has_non_decreasing_digits(number):
    """
    Check if digits never decrease from left to right.

    Args:
        number: A six-digit number

    Returns:
        True if digits are in non-decreasing order
    """
    digits = [int(x) for x in str(number)]
    return digits == sorted(digits)


def solve_part1():
    """
    Count how many passwords meet the criteria within the range.

    The puzzle input range is 158126-624574.
    """
    valid_count = 0
    password_range_start = 158126
    password_range_end = 624574

    for password in range(password_range_start, password_range_end + 1):
        if has_adjacent_matching_digits(password) and has_non_decreasing_digits(password):
            valid_count += 1

    return valid_count


answer = solve_part1()
AoCUtils.print_solution(1, answer)
