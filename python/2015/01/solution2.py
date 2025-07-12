
from aoc_helpers import AoCInput, AoCUtils


def solve_part2():
    content = AoCInput.read_lines("input.txt")[0]
    floor = 0
    buttons = {
        '(': 1,
        ')': -1
    }

    for count, push in enumerate(content):
        floor += buttons[push]
        if floor == -1:
            return count + 1


answer = solve_part2()
AoCUtils.print_solution(2, answer)
