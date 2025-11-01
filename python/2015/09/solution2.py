import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/9/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
from itertools import permutations


def solve_part2():
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

    longest = 0
    for x in permutations(cities.keys(), len(cities.keys())):
        route = [cities[x][y] for x, y in zip(x[:], x[1:])]
        longest = max(longest, sum(route))

    return longest


answer = solve_part2()
AoCUtils.print_solution(2, answer)
