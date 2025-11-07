import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/9/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402


def decompress(s):
    result = 0
    index = 0

    while index < len(s):
        if s[index] != '(':
            result += 1
        else:
            index += 1
            end_marker = index + s[index:].find(')')
            marker = s[index:end_marker]
            characters, repeat = [int(x) for x in marker.split('x')]
            index = end_marker + 1
            substring = s[index:index+characters]
            result += len(substring) * repeat
            index += characters - 1
        index += 1

    return result


def main():
    lines = AoCInput.read_lines(INPUT_FILE)

    for data in lines:
        AoCUtils.print_solution(1, decompress(data.strip()))


if __name__ == "__main__":
    main()
