import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/17/input')

from IntCode import IntCode, InputInterrupt, OutputInterrupt  # noqa: E402
from collections import deque  # noqa: E402


def isIntersection(grid, x, y):
    check = [grid[y+1][x], grid[y-1][x], grid[y][x+1], grid[y][x-1], grid[y][x]]
    return all([x == '#' for x in check])


def solve_part1():
    program = AoCInput.read_file(INPUT_FILE).strip()

    comp1 = IntCode(program)
    comp1.complete = False

    view = []
    while not comp1.complete:
        try:
            comp1.run()
        except OutputInterrupt:
            p = chr(int(comp1.pop()))
            view.append(p)

    grid = []
    for l in ''.join(view).strip().split('\n'):
        grid.append([x for x in l])

    intersections = []
    for y in range(1, len(grid) - 2):
        for x in range(1, len(grid[y]) - 1):
            if grid[y][x] == '#' and isIntersection(grid, x, y):
                intersections.append((x, y))

    result = sum([x*y for x, y in intersections])
    return result


def solve_part2():
    program = AoCInput.read_file(INPUT_FILE).strip()

    # solved this one by hand from printing out the above
    move_routine = "A,B,A,B,A,C,B,C,A,C\n"
    A = "L,6,R,12,L,6\n"
    B = "R,12,L,10,L,4,L,6\n"
    C = "L,10,L,10,L,4,L,6\n"
    video = "n\n"

    comp2 = IntCode(program)
    comp2.complete = False
    comp2.memory[0] = 2

    for s in [move_routine, A, B, C, video]:
        for c in s:
            comp2.push(ord(c))

    display = []
    while not comp2.complete:
        try:
            comp2.run()
        except OutputInterrupt:
            p = chr(int(comp2.pop()))
            display.append(p)

    result = ord(display[-1])
    return result


answer1 = solve_part1()
AoCUtils.print_solution(1, f"The sum of the alignment parameters is: {answer1}")

answer2 = solve_part2()
AoCUtils.print_solution(2, f"The vacuum robot collected {answer2} units of space dust")
