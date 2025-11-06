import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/8/input')


def solve_part1():
    lines = AoCInput.read_lines(INPUT_FILE)

    diff = 0
    for line in lines:
        line = line.strip()
        processed = bytes(line, "utf-8").decode("unicode_escape")
        if processed[0] == '"':
            processed = processed[1:]
        if processed[-1] == '"':
            processed = processed[:-1]
        diff += len(line) - len(processed)

    return diff


answer = solve_part1()
AoCUtils.print_solution(1, answer)
