import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/17/input')


def solve_part1():
    lines = AoCInput.read_lines(INPUT_FILE)

    eggnog = 150

    containers = [int(x) for x in lines]

    valid_combos = 0

    for x in range(1, 2 ** len(containers)):
        mask = str(bin(x))[2:].zfill(len(containers))
        mask = [int(x) for x in mask]
        container_value = sum(x * y for x, y in zip(mask, containers))

        if container_value == eggnog:
            valid_combos += 1

    return valid_combos


answer = solve_part1()
AoCUtils.print_solution(1, answer)
