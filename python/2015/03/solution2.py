import os
import sys
from collections import defaultdict

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/3/input')


def solve_part2():
    lines = AoCInput.read_lines(INPUT_FILE)
    path = lines[0].strip()

    move = {"^": (0, 1), ">": (1, 0), "v": (0, -1), "<": (-1, 0)}

    houses = defaultdict(int)

    santa_location = (0, 0)
    robo_location = (0, 0)

    locations = [santa_location, robo_location]

    for loc in locations:
        houses[loc] += 1

    for idx, house in enumerate(path):
        turn = idx % 2

        locations[turn] = tuple([x + y for x, y in zip(locations[turn], move[house])])
        houses[locations[turn]] += 1

    return len(houses.keys())


answer = solve_part2()
AoCUtils.print_solution(2, answer)
