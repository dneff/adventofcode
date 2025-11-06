import os
import sys
import json

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/12/input')


def getValue(data):
    result = 0
    if isinstance(data, str) or isinstance(data, int):
        try:
            return int(data)
        except ValueError:
            pass
    elif isinstance(data, list):
        for d in data:
            result += getValue(d)
    elif isinstance(data, dict):
        if 'red' not in data.values():
            for d in data.values():
                result += getValue(d)

    return result


def solve_part2():
    lines = AoCInput.read_lines(INPUT_FILE)

    json_data = lines[0]
    data = json.loads(json_data)

    return getValue(data)


answer = solve_part2()
AoCUtils.print_solution(2, answer)
