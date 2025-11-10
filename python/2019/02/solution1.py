import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/2/input')


def advanceReader(x):
    return x + 4


def add(inst, prog):
    prog[inst[2]] = prog[inst[0]] + prog[inst[1]]


def multiply(inst, prog):
    prog[inst[2]] = prog[inst[0]] * prog[inst[1]]


def solve_part1():
    content = AoCInput.read_file(INPUT_FILE)
    prog = [int(x) for x in content.strip().split(',')]

    reader = 0

    while True:
        instruction = prog[reader]
        if instruction == 99:
            break
        elif instruction == 1:
            add(prog[reader+1:reader+4], prog)
        elif instruction == 2:
            multiply(prog[reader+1:reader+4], prog)

        reader = advanceReader(reader)

    return prog[0]


answer = solve_part1()
AoCUtils.print_solution(1, answer)