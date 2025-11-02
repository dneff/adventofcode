import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/24/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
from copy import deepcopy
from collections import defaultdict


def sum_bridge(b):
    """ return sum of a set of tuples"""
    sum_tuple = [sum(x) for x in zip(*b)]
    return sum(sum_tuple)


def get_bridge(pipes, bridge, connector):
    """construct bridges from pipes and return score"""
    if len(pipes) == 0:
        return sum_bridge(bridge)

    bridges = defaultdict(list)
    for p in pipes:
        if connector in p:
            if p.index(connector) == 0:
                next_connector = p[1]
            else:
                next_connector = p[0]
            next_pipes = deepcopy(pipes)
            next_pipes.remove(p)
            next_bridge = deepcopy(bridge)
            next_bridge.append(deepcopy(p))
            b = get_bridge(next_pipes, next_bridge, next_connector)
            bridges[len(b)].append(b)

    if len(bridges.keys()) == 0:
        return bridge

    longest = max(bridges.keys())
    best = [sum_bridge(x) for x in bridges[longest]]
    best_idx = best.index(max(best))
    return bridges[longest][best_idx]


def main():
    lines = AoCInput.read_lines(INPUT_FILE)

    pipes = set()
    for line in lines:
        a, b = [int(x) for x in line.split('/')]
        pipes.add((a, b))

    starting_pipes = set()

    for x in pipes:
        if x[0] == 0:
            starting_pipes.add(x)

    pipes = pipes.difference(starting_pipes)

    bridges = defaultdict(list)
    for p in starting_pipes:
        next_pipes = pipes.difference(p)
        if p.index(0) == 0:
            next_connector = p[1]
        else:
            next_connector = p[0]
        next_bridge = []
        next_bridge.append(deepcopy(p))

        b = get_bridge(next_pipes, next_bridge, next_connector)
        bridges[len(b)].append(b)

    longest = max(bridges.keys())
    best = [sum_bridge(x) for x in bridges[longest]]
    best_idx = best.index(max(best))

    final = bridges[longest][best_idx]

    AoCUtils.print_solution(2, sum_bridge(final))


if __name__ == "__main__":
    main()
