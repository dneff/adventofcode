import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCUtils  # noqa: E402


def hasPair(number):
    digits = ['?'] + [x for x in str(number)] + ['?']
    for index in range(1, 6):
        if digits[index] == digits[index + 1] and \
           digits[index] != digits[index - 1] and \
           digits[index + 1] != digits[index + 2]:
            return True

    return False


def isOrdered(number):
    digits = [int(x) for x in str(number)]
    return digits == sorted(digits)


def solve_part1():
    count = 0
    start, end = 158126, 624574
    for number in range(start, end):
        if hasPair(number) and isOrdered(number):
            count += 1
    return count


answer = solve_part1()
AoCUtils.print_solution(1, answer)