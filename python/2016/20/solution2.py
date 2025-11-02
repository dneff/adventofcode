def AoCUtils.print_solution(2, x):
    print(f"The solution is {x}")
def main():
    blacklist = {}
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/20/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils

        for l in f.readlines():
            begin, end = l.strip().split('-')
            blacklist[int(begin)] = int(end)

    whitelist_floor = 0
    whitelisted = set()

    while len(blacklist.keys()) > 0:
        while len(blacklist.keys()) > 0 and min(blacklist.keys()) <= whitelist_floor:
            whitelist_floor = max(whitelist_floor, blacklist[min(blacklist.keys())] + 1)
            blacklist.pop(min(blacklist.keys()))

        if len(blacklist.keys()) > 0:
            whitelisted.add(whitelist_floor)
            whitelist_floor += 1

    AoCUtils.print_solution(2, len(whitelisted))

if __name__ == "__main__":
    main()