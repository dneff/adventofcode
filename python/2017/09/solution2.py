import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/9/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def filter_garbage(stream):
    """return all garbage from string"""
    clean = []
    unclean = []
    offset = 0
    garbage = False
    while offset < len(stream):
        if stream[offset] == '!':
            offset += 1
        elif stream[offset] == '<':
            if garbage is False:
                garbage = True
            else:
                unclean.append(stream[offset])
        elif stream[offset] == '>':
            garbage = False
        elif garbage is False:
            clean.append(stream[offset])
        elif garbage is True:
            unclean.append(stream[offset])
        offset += 1
    return ''.join(unclean)


def main():
    stream = AoCInput.read_lines(INPUT_FILE)[0].strip()
    AoCUtils.print_solution(2, len(filter_garbage(stream)))


if __name__ == "__main__":
    main()
