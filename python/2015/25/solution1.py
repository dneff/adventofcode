import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/25/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def nextCode(x):
    if x == 0:
        return 20151125
    else:
        return (x * 252533) % 33554393


def getIterations(row, col):
    max_row = row + col - 1
    iterations = sum([x for x in range(max_row)])
    iterations += col
    return iterations


def solve_part1():
    code_loc = (2978, 3083)

    code = 0
    for _ in range(getIterations(*code_loc)):
        code = nextCode(code)

    return code

answer = solve_part1()
AoCUtils.print_solution(1, answer)
