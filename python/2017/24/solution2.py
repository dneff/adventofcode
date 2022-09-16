from copy import deepcopy
from collections import defaultdict


def print_solution(x):
    """format solution for printing"""
    print(f"The solution is: {x}")


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
    file = open('input.txt', 'r', encoding='utf-8')
    pipes = set()
    for line in file.readlines():
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

    print_solution(sum_bridge(final))


if __name__ == "__main__":
    main()
