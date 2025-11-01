import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/24/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
from itertools import combinations
from functools import reduce


def solve_part2():

    lines = AoCInput.read_lines(INPUT_FILE)
    numbers = [int(x) for x in lines]
    target = sum(numbers) // 4

    max_len = 1
    while sum(numbers[:max_len]) <= target:
        max_len += 1
    min_len = 1
    while sum(numbers[-min_len:]) <= target:
        min_len += 1

    buckets = set()
    min_combo = len(numbers)
    qe = {}

    for l in range(min_len, max_len + 1):
        combos = combinations(numbers, l)
        for x in combos:
            if sum(x) == target:
                buckets.add(x)
                min_combo = min(min_combo, len(x))
                qe[reduce((lambda a, b: a*b), x)] = x

    print(min(qe))

answer = solve_part2()
AoCUtils.print_solution(2, answer)
