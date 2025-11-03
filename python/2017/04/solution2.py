"""
Advent of Code 2017 - Day 4: High-Entropy Passphrases (Part 2)

Validate passphrases with an additional security policy: no two words can be anagrams of each
other. A valid passphrase contains no duplicate words and no words that are anagrams of other
words in the passphrase.

Examples:
    - "abcde fghij" is valid (no anagrams)
    - "abcde xyz ecdab" is invalid ("abcde" and "ecdab" are anagrams)
    - "a ab abc abd abf abj" is valid (no anagrams)
    - "iiii oiii ooii oooi oooo" is valid (all different)
    - "oiii ioii iioi iiio" is invalid (all are anagrams of each other)
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/4/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def is_valid_passphrase_no_anagrams(passphrase):
    """
    Check if a passphrase is valid (no duplicate words and no anagrams).

    Args:
        passphrase: String containing space-separated words

    Returns:
        True if all words are unique and no anagrams exist, False otherwise
    """
    # Sort each word's letters to normalize anagrams
    normalized_words = [''.join(sorted(word)) for word in passphrase.strip().split()]
    return len(normalized_words) == len(set(normalized_words))


def main():
    """Count how many passphrases are valid (no duplicates or anagrams)."""
    passphrases = AoCInput.read_lines(INPUT_FILE)
    valid_count = 0

    for passphrase in passphrases:
        if is_valid_passphrase_no_anagrams(passphrase):
            valid_count += 1

    AoCUtils.print_solution(2, valid_count)


if __name__ == "__main__":
    main()
