import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/1/input')


def moduleFuel(mass):
    return (mass // 3) - 2


def solve_part1():
    lines = AoCInput.read_lines(INPUT_FILE)
    result = 0

    for line in lines:
        result += moduleFuel(int(line.strip()))

    return result


answer = solve_part1()
AoCUtils.print_solution(1, answer)
