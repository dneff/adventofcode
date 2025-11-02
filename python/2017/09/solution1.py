import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/9/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def clean_garbage(stream):
    """remove all garbage from string"""
    clean = []
    offset = 0
    garbage = False
    while offset < len(stream):
        if stream[offset] == '<':
            garbage = True
        elif stream[offset] == '!':
            offset += 1
        elif stream[offset] == '>':
            garbage = False
        elif garbage is False:
            clean.append(stream[offset])
        offset += 1
    return ''.join(clean)


def score_stream(stream):
    """ score brackets in stream """
    score = 0
    depth = 0
    offset = 0
    while offset < len(stream):
        if stream[offset] == '{':
            depth += 1
        elif stream[offset] == '}':
            score += depth
            depth -= 1
        offset += 1

    return score


def main():
    stream = AoCInput.read_lines(INPUT_FILE)[0].strip()
    stream = clean_garbage(stream)
    AoCUtils.print_solution(1, score_stream(stream))


if __name__ == "__main__":
    main()
