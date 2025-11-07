import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/4/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402
import re  # noqa: E402
import string  # noqa: E402
from collections import defaultdict  # noqa: E402


def isRealRoom(name, checksum):
    count = defaultdict(int)
    for c in name:
        if c == "-":
            continue
        count[c] += 1

    frequency = defaultdict(list)
    for k, v in count.items():
        frequency[v].append(k)

    generated_sum = []
    for k in sorted(frequency.keys(), reverse=True):
        generated_sum.extend(sorted(frequency[k]))
    generated_sum = "".join([str(x) for x in generated_sum])
    if generated_sum[:5] == checksum:
        return True
    return False


def shiftCipher(s, rotations):
    result = []
    words = s.split("-")
    for word in words:
        for c in word:
            val = string.ascii_lowercase.find(c)
            new_val = (val + rotations) % len(string.ascii_lowercase)
            new_char = string.ascii_lowercase[new_val]
            result.append(new_char)
        result.append(" ")
    return "".join(result)


def main():
    lines = AoCInput.read_lines(INPUT_FILE)

    words = defaultdict(int)
    sectors = {}
    for line in lines:
        sector = re.search(r"(\d+)", line)[0]
        checksum = re.search(r"\[(.*)\]", line).group(1)
        name = line.split(sector)[0]
        if isRealRoom(name, checksum):
            sectors[sector] = shiftCipher(name, int(sector))
            for word in sectors[sector].split():
                words[word] += 1
    unique = []
    for k, v in words.items():
        if v == 1:
            unique.append(k)
    for k, v in sectors.items():
        if unique[0] in v:
            AoCUtils.print_solution(2, k)


if __name__ == "__main__":
    main()
