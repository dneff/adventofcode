import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/20/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def getFactors(x):
    results = []
    for i in range(1, int(x ** 0.5) + 1):
        if x % i == 0:
            results.extend([i, x // i])
    return set(results)


def solve_part1():

    target_presents = 36000000
    house_number = 0

    delivering = True

    while delivering:
        house_number += 1
        visiting_elves = getFactors(house_number)
        presents_delivered = sum([10 * elf for elf in visiting_elves])
        delivering = presents_delivered <= target_presents

    return house_number

answer = solve_part1()
AoCUtils.print_solution(1, answer)
