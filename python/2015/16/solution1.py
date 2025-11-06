import os
import sys
from collections import defaultdict

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/16/input')


def solve_part1():
    lines = AoCInput.read_lines(INPUT_FILE)

    detected = {
        "children": 3,
        "cats": 7,
        "samoyeds": 2,
        "pomeranians": 3,
        "akitas": 0,
        "vizslas": 0,
        "goldfish": 5,
        "trees": 3,
        "cars": 2,
        "perfumes": 1,
    }

    aunts = {}
    matches = defaultdict(int)
    for line in lines:
        line = line.strip().lstrip("Sue ")
        line = line.replace(":", "").replace(",", "")
        line = line.split()

        aunt = int(line.pop(0))
        aunts[aunt] = {}
        while line:
            k, v = line.pop(0), line.pop(0)
            aunts[aunt][k] = int(v)

    for aunt, details in aunts.items():
        for k, v in details.items():
            if k in detected and detected[k] == v:
                matches[aunt] += 1

    return max(matches, key=matches.get)


answer = solve_part1()
AoCUtils.print_solution(1, answer)
