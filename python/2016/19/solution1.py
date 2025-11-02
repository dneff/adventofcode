import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/19/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils

def AoCUtils.print_solution(1, x):
    print(f"The solution is {x}")
def main():
    test = 5
    puzzle1 = 3004953
    active = puzzle1
    elves = list(range(1, active + 1))

    while len(elves) != 1:
        extra = len(elves) % 2 == 1

        elves = elves[::2]
        if extra:
            elves.pop(0)

    AoCUtils.print_solution(1, elves[0])

if __name__ == "__main__":
    main()