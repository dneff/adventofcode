import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/3/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
from collections import defaultdict


def solve_part1():
    lines = AoCInput.read_lines(INPUT_FILE)
    path = lines[0].strip()

    move = {"^": (0, 1), ">": (1, 0), "v": (0, -1), "<": (-1, 0)}

    houses = defaultdict(int)

    location = (0, 0)
    houses[location] += 1

    for house in path:
        location = tuple([x+y for x, y in zip(location, move[house])])
        houses[location] += 1

    return len(houses.keys())


answer = solve_part1()
AoCUtils.print_solution(1, answer)
