
from aoc_helpers import AoCInput, AoCUtils


def solve_part1():
    content = AoCInput.read_lines("input.txt")[0]
    floor = 0
    buttons = {
        '(': 1,
        ')': -1
    }

    for push in content:
        floor += buttons[push]

    return floor


answer = solve_part1()
AoCUtils.print_solution(1, answer)
