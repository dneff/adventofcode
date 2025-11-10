import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/16/input')


def processData(data, phases=1):

    base = [0, 1, 0, -1]

    result = []
    p_data = [int(x) for x in data]

    for _ in range(1, phases + 1):
        result = []
        for rounds in range(1, len(data) + 1):
            digit = 0
            for i, d in enumerate(p_data):
                base_pos = ((i + 1)//rounds) % len(base)
                digit += d * base[base_pos]
            result.append(abs(digit) % 10)
        p_data = result[:]

    return "".join([str(x) for x in result])


def processDataP2(data, phases=100):
    full_data = data * 10000
    offset_idx = int(data[:7])
    trunc_data = full_data[offset_idx:]

    result = []
    p_data = [int(x) for x in trunc_data]

    for _ in range(1, phases + 1):
        result = [0] * len(p_data)
        result[-1] = p_data[-1]
        for idx in range(len(p_data) - 2, -1, -1):
            result[idx] = (p_data[idx] + result[idx+1]) % 10
        p_data = result[:]

    return "".join([str(x) for x in result])


def solve_part1():
    data = AoCInput.read_file(INPUT_FILE).strip()
    result = processData(data, 100)[:8]
    return result


def solve_part2():
    data = AoCInput.read_file(INPUT_FILE).strip()
    result = processDataP2(data, 100)[:8]
    return result


answer1 = solve_part1()
AoCUtils.print_solution(1, f"The first eight digits of the final output list after 100 FFT phases is {answer1}")

answer2 = solve_part2()
AoCUtils.print_solution(2, f"The eight-digit message is {answer2}")
