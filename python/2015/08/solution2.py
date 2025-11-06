import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/8/input')


def solve_part2():
    lines = AoCInput.read_lines(INPUT_FILE)

    original = []
    reencoded = []

    for line in lines:
        original.append(line.strip())

        encoded = line.strip()
        encoded = encoded.encode("ascii", "backslashreplace").replace(b"\\", b"\\\\").replace(b'"', b'\\"')
        encoded = b'"' + encoded + b'"'
        reencoded.append(encoded)

    diff = [len(x) - len(y) for x, y in zip(reencoded, original)]

    return sum(diff)


answer = solve_part2()
AoCUtils.print_solution(2, answer)
