import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/13/input')

from IntCode import IntCode, OutputInterrupt, InputInterrupt  # noqa: E402


def solve_part1():
    program = AoCInput.read_file(INPUT_FILE).strip()

    comp1 = IntCode(program)

    screen = {}

    while not comp1.complete:
        try:
            comp1.run()
        except(OutputInterrupt):
            if len(comp1.output) == 3:
                x, y, id = comp1.output
                screen[(x, y)] = id

                comp1.output.clear()

    block_count = len([x for x in screen.values() if x == 2])
    return block_count


def solve_part2():
    program = AoCInput.read_file(INPUT_FILE).strip()

    def joystickTilt(ball, paddle):
        j_tilt = 0
        if ball[0] < paddle[0]:
            j_tilt -= 1
        elif ball[0] > paddle[0]:
            j_tilt += 1
        return j_tilt

    ball = (0, 0)
    paddle = (0, 0)
    score = 0

    comp2 = IntCode(program)
    comp2.memory[0] = 2

    screen = {}

    while not comp2.complete:
        try:
            comp2.run()
        except(InputInterrupt):
            comp2.push(joystickTilt(ball, paddle))
        except(OutputInterrupt):
            if len(comp2.output) == 3:
                x, y, id = comp2.output

                if (x, y) == (-1, 0):
                    score = id
                elif id == 3:
                    paddle = (x, y)
                elif id == 4:
                    ball = (x, y)

                screen[(x, y)] = id

                comp2.output.clear()

    return score


answer1 = solve_part1()
AoCUtils.print_solution(1, f"The block count on exit is: {answer1}")

answer2 = solve_part2()
AoCUtils.print_solution(2, f"The final score is {answer2}")
