import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/19/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
import re
from collections import defaultdict


def solve_part1():

    replacements = defaultdict(list)
    lines = AoCInput.read_lines(INPUT_FILE)
    for line in lines:
        if not line.strip():
            break
        start, end = line.strip().split(" => ")
        replacements[start].append(end)

    molecule = lines[0].strip()
    created = set()
    for element in replacements:
        element_locs = [loc.span() for loc in re.finditer(element, molecule)]
        for loc in element_locs:
            for substitution in replacements[element]:
                created.add(molecule[:loc[0]] + substitution + molecule[loc[1]:])

    return len(created)

answer = solve_part1()
AoCUtils.print_solution(1, answer)
