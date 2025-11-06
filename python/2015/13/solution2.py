import os
import sys
from collections import defaultdict
from itertools import permutations

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/13/input')


def solve_part2():
    lines = AoCInput.read_lines(INPUT_FILE)

    happiness = defaultdict(dict)

    for line in lines:
        line = line.strip().strip(".")
        if "would lose" in line:
            line = line.replace("would lose ", "-").split()
        else:
            line = line.replace("would gain ", "").split()
        subject, difference, guest = line[0], int(line[1]), line[-1]

        happiness[subject][guest] = difference

    guests = [x for x in happiness.keys()]
    for guest in guests:
        happiness["me"][guest] = 0
        happiness[guest]["me"] = 0

    most_happy = 0
    for seating in permutations(happiness.keys()):
        table_happiness = sum([happiness[x][y] + happiness[y][x] for x, y in zip(seating, seating[1:])])
        table_happiness += happiness[seating[0]][seating[-1]] + happiness[seating[-1]][seating[0]]
        most_happy = max(most_happy, table_happiness)

    return most_happy


answer = solve_part2()
AoCUtils.print_solution(2, answer)
