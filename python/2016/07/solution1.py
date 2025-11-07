import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/7/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402
import re  # noqa: E402


def hasABBA(s):
    for i in range(1, len(s)-2):
        if s[i] == s[i+1] and s[i-1] == s[i+2]:
            if s[i] != s[i-1]:
                return True
    return False


def main():

    support_tls = []
    lines = AoCInput.read_lines(INPUT_FILE)

    for line in lines:
        hypernet = []
        for s in re.findall(r"(\[\w*\])", line):
            if s[0] == '[':
                hypernet.append(s.strip('[]'))

        if any([hasABBA(s) for s in hypernet]):
            continue

        ip = []
        for s in re.split(r"\[|\]", line.strip()):
            if s not in hypernet:
                ip.append(s)
        if any([hasABBA(s) for s in ip]):
            pass
        else:
            continue
        support_tls.append(line.strip())

    AoCUtils.print_solution(1, len(support_tls))


if __name__ == "__main__":
    main()
