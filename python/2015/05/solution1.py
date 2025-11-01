import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/5/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
from collections import defaultdict


def propertyOne(s):
    """checks string contains at least 3 vowels"""
    chars = defaultdict(int)
    for c in s:
        chars[c] += 1

    vowel_count = sum([chars[x] for x in ["a", "e", "i", "o", "u"]])

    return vowel_count >= 3


def propertyTwo(s):
    """checks at least one letter appears twice in a row"""
    for idx, c in enumerate(s):
        if idx == 0:
            continue
        if c == s[idx - 1]:
            return True
    return False


def propertyThree(s):
    """checks no forbidden pairs are in string"""
    bad_pairs = ["ab", "cd", "pq", "xy"]
    for pair in bad_pairs:
        if pair in s:
            return False
    return True


def solve_part1():
    lines = AoCInput.read_lines(INPUT_FILE)

    nice = []
    naughty = []

    for line in lines:
        line = line.strip()
        if all([propertyOne(line), propertyTwo(line), propertyThree(line)]):
            nice.append(line)
        else:
            naughty.append(line)

    return len(nice)


answer = solve_part1()
AoCUtils.print_solution(1, answer)
