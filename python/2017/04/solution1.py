"""
Advent of Code 2017 - Day 4: High-Entropy Passphrases (Part 1)

Validate passphrases based on a security policy that requires no duplicate words.
A valid passphrase contains only unique words (space-separated).

Examples:
    - "aa bb cc dd ee" is valid (all words are unique)
    - "aa bb cc dd aa" is invalid (word "aa" appears twice)
    - "aa bb cc dd aaa" is valid ("aa" and "aaa" are different words)
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/4/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402


def is_valid_passphrase(passphrase):
    """
    Check if a passphrase is valid (contains no duplicate words).

    Args:
        passphrase: String containing space-separated words

    Returns:
        True if all words are unique, False otherwise
    """
    words = passphrase.strip().split()
    return len(words) == len(set(words))


def main():
    """Count how many passphrases are valid (no duplicate words)."""
    passphrases = AoCInput.read_lines(INPUT_FILE)
    valid_count = 0

    for passphrase in passphrases:
        if is_valid_passphrase(passphrase):
            valid_count += 1

    AoCUtils.print_solution(1, valid_count)


if __name__ == "__main__":
    main()
