"""
Advent of Code 2017 - Day 9: Stream Processing (Part 1)

Process a stream of characters containing groups and garbage. Groups are delimited by
curly braces {} and can be nested. Garbage is delimited by angle brackets <> and should
be removed before scoring. Inside garbage, ! cancels the next character.

Score each group by its nesting depth, then sum all group scores.

Examples:
    {} = 1 (one group at depth 1)
    {{{}}} = 1 + 2 + 3 = 6 (three nested groups)
    {{},{}} = 1 + 2 + 2 = 5 (one group at depth 1, two at depth 2)
    {{{},{},{{}}}} = 1 + 2 + 3 + 3 + 3 + 4 = 16

Garbage examples:
    <> = empty garbage
    <random characters> = garbage containing "random characters"
    <<<<> = garbage containing "<<<" (< doesn't end garbage)
    <{!>}> = garbage containing "{" (the > was canceled)
    <!!> = empty garbage (both ! cancel each other)
    <!!!>> = empty garbage
    <{o"i!a,<{i<a> = garbage containing {o"i,<{i<a
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/9/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def remove_garbage(stream):
    """
    Remove all garbage from the stream, including escape sequences.

    Garbage is anything between < and >, where ! escapes the next character.

    Args:
        stream: String containing groups and garbage

    Returns:
        Clean string with only group delimiters and commas
    """
    clean = []
    offset = 0
    in_garbage = False

    while offset < len(stream):
        if stream[offset] == '<':
            in_garbage = True
        elif stream[offset] == '!':
            offset += 1  # Skip the next character
        elif stream[offset] == '>':
            in_garbage = False
        elif not in_garbage:
            clean.append(stream[offset])
        offset += 1

    return ''.join(clean)


def calculate_group_score(stream):
    """
    Calculate the total score of all groups in the stream.

    Each group's score equals its nesting depth. The score is the sum of all group scores.

    Args:
        stream: Clean string containing only {} and commas

    Returns:
        Total score of all groups
    """
    total_score = 0
    nesting_depth = 0
    offset = 0

    while offset < len(stream):
        if stream[offset] == '{':
            nesting_depth += 1
        elif stream[offset] == '}':
            total_score += nesting_depth
            nesting_depth -= 1
        offset += 1

    return total_score


def main():
    """Process stream and calculate total group score."""
    stream = AoCInput.read_lines(INPUT_FILE)[0].strip()
    clean_stream = remove_garbage(stream)
    score = calculate_group_score(clean_stream)
    AoCUtils.print_solution(1, score)


if __name__ == "__main__":
    main()
