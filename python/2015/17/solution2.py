import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/17/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
from collections import defaultdict


def solve_part2():
    lines = AoCInput.read_lines(INPUT_FILE)

    eggnog = 150

    containers = [int(x) for x in lines]

    combo_size = defaultdict(int)

    for x in range(1, 2 ** len(containers)):
        mask = str(bin(x))[2:].zfill(len(containers))
        mask = [int(x) for x in mask]
        container_value = sum(x * y for x, y in zip(mask, containers))

        if container_value == eggnog:
            combo_size[sum(mask)] += 1

    return combo_size[min(combo_size.keys())]


answer = solve_part2()
AoCUtils.print_solution(2, answer)
