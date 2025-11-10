import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/19/input')

from IntCode import IntCode, InputInterrupt, OutputInterrupt  # noqa: E402
import math  # noqa: E402


def getAngle(point):
    x, y = point
    theta = (math.degrees(math.atan2(y, x)) + 90) % 360

    return round(theta, 3)


def inBeam(program, point):
    comp1 = IntCode(program)
    x, y = point
    comp1.push(x)
    comp1.push(y)
    try:
        comp1.run()
    except OutputInterrupt:
        o = comp1.pop()
    return o == 1


def solve_part1():
    program = AoCInput.read_file(INPUT_FILE).strip()

    affected = []
    for y in range(50):
        lead_edge = 0
        edge_found = False
        for x in range(50):
            if x < lead_edge:
                continue
            comp1 = IntCode(program)
            comp1.push(x)
            comp1.push(y)
            try:
                comp1.run()
            except OutputInterrupt:
                o = comp1.pop()
                if o == 1:
                    affected.append((x, y))
                    if edge_found is False:
                        edge_found = True
                        lead_edge = x
                elif o == 0 and lead_edge is True:
                    break

    return len(affected), affected


def solve_part2(affected):
    program = AoCInput.read_file(INPUT_FILE).strip()

    # compute angular edges of tractor beam to approximate edge locations further out
    top = (0, 0)
    bottom = (0, 0)
    for p in affected:
        if p[0] > top[0]:
            top = p
        if p[1] > bottom[1]:
            bottom = p
    min_angle = min(getAngle(top), getAngle(bottom))
    max_angle = max(getAngle(top), getAngle(bottom))

    # walk top edge of tractor beam and check dimensions
    # tractor beam has to be at least 100 wide at first possible target
    start_y = 200
    start_x = 0
    result = 0
    while True:
        x = 0
        y = start_y
        l_edge = 0
        r_edge = 0
        while r_edge == 0:
            x += 1
            if getAngle((x, y)) > max_angle:
                continue
            if getAngle((x, y)) <= max_angle and l_edge == 0:
                l_edge = x
            elif getAngle((x, y)) < min_angle:
                r_edge = x
        if r_edge - l_edge > 100:
            start_x = r_edge
            break
        start_y += 1
    # now we'll start checking edge values looking for 2 corners to fit
    while True:
        if inBeam(program, (start_x, start_y)):
            start_x += 1
            continue
        start_x -= 1
        if inBeam(program, (start_x - 99, start_y + 99)):
            result = (start_x - 99) * 10000 + start_y
            break
        else:
            start_y += 1

    return result


answer1, affected = solve_part1()
AoCUtils.print_solution(1, f"There are {answer1} points affected by the tractor beam")

answer2 = solve_part2(affected)
AoCUtils.print_solution(2, f"The coded point closest to the tractor beam is {answer2}")
