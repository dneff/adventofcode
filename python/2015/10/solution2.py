import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/10/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


class LookSay():
    def __init__(self, start):
        self.sequence = ''

        if len(start) == 0:
            raise ValueError("starting value should be at least one digit")

        self.sequence = start

    def step(self):
        updated = ''
        counter = 1
        if len(self.sequence) == 1:
            updated = str(counter) + self.sequence
        else:
            for idx, digit in enumerate(self.sequence[1:]):
                if digit == self.sequence[idx]:
                    counter += 1
                else:
                    updated += str(counter) + self.sequence[idx]
                    counter = 1
            updated += str(counter) + self.sequence[-1]

        self.sequence = updated


def solve_part2():
    lines = AoCInput.read_lines(INPUT_FILE)
    input = lines[0].strip()
    turns = 50

    game = LookSay(input)
    for i in range(1, turns + 1):
        game.step()

    return len(game.sequence)


answer = solve_part2()
AoCUtils.print_solution(2, answer)
