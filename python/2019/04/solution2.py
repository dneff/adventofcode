"""
Advent of Code 2019 - Day 4: Secure Container
Part 2: Count valid passwords with stricter adjacent digit rule.

The password criteria are updated:
- Two adjacent matching digits must NOT be part of a larger group
  (e.g., 112233 is valid, but 123444 is not because 444 is a group of 3)
- Digits still must never decrease
- The value is still within the puzzle input range

Examples:
- 112233 is valid (has pairs 11, 22, 33)
- 123444 is invalid (444 is a group of 3, not a pair)
- 111122 is valid (has pair 22, even though 1111 is a larger group)
"""
import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCUtils  # noqa: E402


def has_exact_pair(number):
    """
    Check if the number has at least one pair of adjacent matching digits
    that is NOT part of a larger group.

    Uses sentinel characters '?' at the boundaries to simplify edge checking.

    Args:
        number: A six-digit number

    Returns:
        True if there's at least one exact pair (not part of a larger group)
    """
    # Add sentinel characters to avoid boundary checks
    digits = ['?'] + [x for x in str(number)] + ['?']

    # Check each adjacent pair
    for i in range(1, 6):
        # Check if current and next digit match
        # AND are not part of a larger group (check neighbors)
        if (digits[i] == digits[i + 1] and
            digits[i] != digits[i - 1] and
                digits[i + 1] != digits[i + 2]):
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


def solve_part2():
    """
    Count how many passwords meet the stricter criteria within the range.

    The puzzle input range is 158126-624574.
    """
    valid_count = 0
    password_range_start = 158126
    password_range_end = 624574

    for password in range(password_range_start, password_range_end + 1):
        if has_exact_pair(password) and has_non_decreasing_digits(password):
            valid_count += 1

    return valid_count


answer = solve_part2()
AoCUtils.print_solution(2, answer)
