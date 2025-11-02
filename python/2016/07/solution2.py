import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/7/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
import re


def getABA(s):
    aba = []
    for i in range(1, len(s)-1):
        if s[i-1] == s[i+1] and s[i-1] != s[i]:
            aba.append(s[i-1:i+2])
    return aba


def invertABA(s):
    return s[1] + s[0] + s[1]


def main():

    support_ssl = []
    lines = AoCInput.read_lines(INPUT_FILE)

    for line in lines:
        hypernet = []
        for s in re.findall("(\[\w*\])", line):
            if s[0] == '[':
                hypernet.append(s.strip('[]'))
        
        abas  = []
        for h in hypernet:
            abas.extend(getABA(h))

        if len(abas) == 0:
            continue

        babs = [invertABA(x) for x in abas]

        ssl_match = []
        for s in re.split("\[|\]", line.strip()):
            if s in hypernet:
                continue
            if len(ssl_match) == 0:
                for bab in babs:
                    if bab in s:
                        ssl_match.append(s)
                        support_ssl.append(line.strip())
                        break

    AoCUtils.print_solution(2, len(set(support_ssl)))
    

if __name__ == "__main__":
    main()
