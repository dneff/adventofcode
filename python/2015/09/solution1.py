import os
import sys
from itertools import permutations

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/9/input')


def solve_part1():
    lines = AoCInput.read_lines(INPUT_FILE)

    cities = {}

    for line in lines:
        c1c2, distance = line.strip().split(" = ")
        c1, c2 = c1c2.split(" to ")
        distance = int(distance)
        for city in [c1, c2]:
            if city not in cities:
                cities[city] = {}
        cities[c1][c2] = distance
        cities[c2][c1] = distance

    shortest = 0
    for x in permutations(cities.keys(), len(cities.keys())):
        route = [cities[x][y] for x, y in zip(x[:], x[1:])]
        if shortest == 0:
            shortest = sum(route)
        else:
            shortest = min(shortest, sum(route))

    return shortest


answer = solve_part1()
AoCUtils.print_solution(1, answer)
