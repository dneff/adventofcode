import os
import sys
from itertools import permutations

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from IntCode import IntCode, InputInterrupt, OutputInterrupt  # noqa: E402
from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/9/input')


def solve_part1():
    program = AoCInput.read_file(INPUT_FILE).strip()

    comp = IntCode(program)
    comp.push(1)

    while not comp.complete:
        try:
            comp.run()
        except(OutputInterrupt):
            pass

    return comp.pop()


def solve_part2():
    program = AoCInput.read_file(INPUT_FILE).strip()

    comp2 = IntCode(program)
    comp2.push(2)

    while not comp2.complete:
        try:
            comp2.run()
        except(OutputInterrupt):
            pass

    return comp2.output[-1]


answer1 = solve_part1()
AoCUtils.print_solution(1, answer1)

answer2 = solve_part2()
AoCUtils.print_solution(2, answer2)
