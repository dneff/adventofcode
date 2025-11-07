"""
Advent of Code 2017 - Day 9: Stream Processing (Part 2)

Count the total number of non-canceled characters within garbage sections. Garbage is
anything between < and >, where ! escapes the next character. The delimiters < and >
themselves don't count, nor do canceled characters or the ! doing the canceling.

Examples:
    <> = 0 characters (empty garbage)
    <random characters> = 17 characters
    <<<<> = 3 characters (the first three < are garbage)
    <{!>}> = 2 characters ({ and }, the > was canceled)
    <!!> = 0 characters (both ! cancel each other)
    <!!!>> = 0 characters (first ! cancels second, third ! cancels first >)
    <{o"i!a,<{i<a> = 10 characters
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/9/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402


def count_garbage_characters(stream):
    """
    Count non-canceled characters within garbage sections.

    Garbage is delimited by < and >. The ! character cancels the next character.
    Only count characters between delimiters, excluding canceled ones.

    Args:
        stream: String containing groups and garbage

    Returns:
        Count of non-canceled garbage characters (excluding delimiters)
    """
    garbage_count = 0
    offset = 0
    in_garbage = False

    while offset < len(stream):
        if stream[offset] == '!':
            offset += 1  # Skip the next character entirely
        elif stream[offset] == '<':
            if in_garbage:
                # We're already in garbage, so this < is a garbage character
                garbage_count += 1
            else:
                # Start of new garbage section
                in_garbage = True
        elif stream[offset] == '>':
            # End of garbage section (don't count the >)
            in_garbage = False
        elif in_garbage:
            # Regular character inside garbage
            garbage_count += 1
        offset += 1

    return garbage_count


def main():
    """Count and print total garbage characters."""
    stream = AoCInput.read_lines(INPUT_FILE)[0].strip()
    garbage_count = count_garbage_characters(stream)
    AoCUtils.print_solution(2, garbage_count)


if __name__ == "__main__":
    main()
