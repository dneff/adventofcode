import os
import sys
import math

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/10/input')


def getAngle(base, asteroid):
    # return r, theta(degrees)
    x = asteroid[0] - base[0]
    y = asteroid[1] - base[1]
    r = (x ** 2 + y**2) ** .5
    theta = (math.degrees(math.atan2(y, x)) + 90) % 360

    return round(r, 3), round(theta, 3)


def solve_part1():
    data = AoCInput.read_lines(INPUT_FILE)

    map = []
    for r, line in enumerate(data):
        for c, val in enumerate(line):
            if val == '#':
                map.append((c, r))
    max_base = (0, 0)
    max_sight = 0

    for base in map:
        angles = {}
        for a in map:
            if base == a:
                continue
            r, d = getAngle(base, a)
            angles[d] = a
        if len(angles.keys()) > max_sight:
            max_base = base
            max_sight = len(angles.keys())

    # Store max_base for part 2
    solve_part1.max_base = max_base
    solve_part1.map = map

    return max_sight


def solve_part2():
    max_base = solve_part1.max_base
    map = solve_part1.map

    sited = {}
    for a in map:
        if max_base == a:
            continue
        r, d = getAngle(max_base, a)
        if d not in sited.keys():
            sited[d] = (a[0], a[1], r)
        else:
            if abs(r) < abs(sited[d][2]):
                sited[d] = (a[0], a[1], r)

    shoot_order = list(sited.keys())
    shoot_order.sort()
    result = sited[shoot_order[199]]
    return result[0] * 100 + result[1]


answer1 = solve_part1()
AoCUtils.print_solution(1, answer1)

answer2 = solve_part2()
AoCUtils.print_solution(2, answer2)
