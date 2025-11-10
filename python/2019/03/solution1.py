import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/3/input')


def endPoint(loc, run):
    x, y = loc
    distance = int(run[1:])

    if run[0] == 'U':
        y += distance
    elif run[0] == 'D':
        y -= distance
    elif run[0] == 'L':
        x -= distance
    elif run[0] == 'R':
        x += distance

    return (x, y)


def findPoints(path):
    pos = [0, 0]
    for i in path:
        for _ in range(int(i[1:])):
            if i[0] == 'L':
                pos[0] += -1
            elif i[0] == 'R':
                pos[0] += 1
            elif i[0] == 'U':
                pos[1] += 1
            elif i[0] == 'D':
                pos[1] += -1

            yield tuple(pos)


def solve_part1():
    lines = AoCInput.read_lines(INPUT_FILE)
    path_a = lines[0].strip().split(',')
    path_b = lines[1].strip().split(',')

    points_a = list(findPoints(path_a))
    points_b = list(findPoints(path_b))

    intersections = set(points_a) & set(points_b)

    solution = min([abs(x) + abs(y) for x, y in intersections])
    return solution


def solve_part2():
    lines = AoCInput.read_lines(INPUT_FILE)
    path_a = lines[0].strip().split(',')
    path_b = lines[1].strip().split(',')

    points_a = list(findPoints(path_a))
    points_b = list(findPoints(path_b))

    intersections = set(points_a) & set(points_b)

    lengths = []
    for intersect in intersections:
        dist = []
        for points in points_a, points_b:
            dist.append(points.index(intersect))

        lengths.append(sum(dist) + 2)

    return min(lengths)


answer1 = solve_part1()
AoCUtils.print_solution(1, answer1)

answer2 = solve_part2()
AoCUtils.print_solution(2, answer2)