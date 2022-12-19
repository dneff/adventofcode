from copy import deepcopy

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

    scores = []
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
            scores.append(get_bridge(next_pipes, next_bridge, next_connector))

    if len(scores) == 0:
        return sum_bridge(bridge)

    return max(scores)


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

    scores = []
    for p in starting_pipes:
            next_pipes = pipes.difference(p)
            if p.index(0) == 0:
                next_connector = p[1]
            else:
                next_connector = p[0]
            next_bridge = []
            next_bridge.append(deepcopy(p))
            scores.append(get_bridge(next_pipes, next_bridge, next_connector))

    print_solution(max(scores))


if __name__ == "__main__":
    main()
