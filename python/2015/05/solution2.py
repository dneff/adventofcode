import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/5/input')


def propertyOne(s):
    """checks if any pair appears twice"""
    for idx in range(1, len(s)):
        pair = s[idx - 1: idx + 1]
        if pair in s[: idx - 1] or pair in s[idx + 1:]:
            return True
    return False


def propertyTwo(s):
    """checks if any character repeats with a letter in between"""
    for idx in range(2, len(s)):
        if s[idx] == s[idx - 2]:
            return True
    return False


def solve_part2():
    lines = AoCInput.read_lines(INPUT_FILE)

    nice = []
    naughty = []

    for line in lines:
        line = line.strip()
        if all([propertyOne(line), propertyTwo(line)]):
            nice.append(line)
        else:
            naughty.append(line)

    return len(nice)


answer = solve_part2()
AoCUtils.print_solution(2, answer)
