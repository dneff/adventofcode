import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/2/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def getWrapping(length, width, height):
    sides = [length * width, width * height, height * length]
    wrapping = 2 * sum(sides)
    slack = min(sides)
    return wrapping + slack


def getRibbon(length, width, height):
    sides = [length + width, width + height, height + length]
    ribbon = 2 * min(sides)
    return ribbon


def getBow(length, width, height):
    bow = length * width * height
    return bow


def solve_part2():
    lines = AoCInput.read_lines(INPUT_FILE)

    total_ribbon = 0
    for line in lines:
        l, w, h = [int(x) for x in line.strip().split("x")]
        total_ribbon += getRibbon(l, w, h)
        total_ribbon += getBow(l, w, h)

    return total_ribbon


answer = solve_part2()
AoCUtils.print_solution(2, answer)
