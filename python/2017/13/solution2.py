import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/13/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def main():
    lines = AoCInput.read_lines(INPUT_FILE)
    firewall = {}
    for line in lines:
        layer, depth = [int(x) for x in line.split(': ')]
        firewall[layer] = depth

    delay = 0
    blocked = True
    while blocked:
        for time in range(max(firewall.keys()) + 1):
            if time in firewall:
                if (time + delay) % ((firewall[time] - 1) * 2) == 0:
                    delay += 1
                    break
            if time >= max(firewall.keys()):
                blocked = False

    AoCUtils.print_solution(2, delay)


if __name__ == "__main__":
    main()
