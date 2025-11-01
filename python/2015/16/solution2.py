import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/16/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
from collections import defaultdict


def scoreAunt(details):
    result = 0
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

    for k, v in details.items():
        if k in ['cats', 'trees']:
            if detected[k] < v:
                result += 1
        elif k in ['pomeranians', 'goldfish']:
            if detected[k] > v:
                result += 1
        else:
            if detected[k] == v:
                result += 1

    return result


def solve_part2():
    lines = AoCInput.read_lines(INPUT_FILE)

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
        matches[aunt] = scoreAunt(details)

    return max(matches, key=matches.get)


answer = solve_part2()
AoCUtils.print_solution(2, answer)
