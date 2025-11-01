import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/4/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
from hashlib import md5


def solve_part2():
    lines = AoCInput.read_lines(INPUT_FILE)
    input = lines[0].strip()
    suffix = 0
    checking = True

    while checking:
        possible = input + str(suffix)
        possible_encoded = md5(possible.encode("utf-8")).hexdigest()
        if possible_encoded[:6] == "000000":
            print(possible_encoded)
            checking = False
            continue
        suffix += 1

    return suffix


answer = solve_part2()
AoCUtils.print_solution(2, answer)
