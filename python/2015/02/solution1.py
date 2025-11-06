import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/2/input')


def getWrapping(length, width, height):
    sides = [length * width, width * height, height * length]
    wrapping = 2 * sum(sides)
    slack = min(sides)
    return wrapping + slack


def solve_part1():
    lines = AoCInput.read_lines(INPUT_FILE)

    total_wrapping = 0
    for line in lines:
        l, w, h = [int(x) for x in line.strip().split("x")]
        total_wrapping += getWrapping(l, w, h)

    return total_wrapping


answer = solve_part1()
AoCUtils.print_solution(1, answer)
