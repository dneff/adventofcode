"""solution to 2023 Day 8 solution 2"""
import re
from math import lcm

def print_solution(x):
    """prints solution"""
    print(f"The solution is {x}")


def get_next(path):
    """loops on path"""
    idx = 0
    count = len(path)
    while path:
        yield path[idx]
        idx = (idx + 1) % count


def get_steps(path, start, network):
    """gets steps from start to node ending in Z"""
    trail = get_next(path)
    current = start
    steps = 0

    while current[-1] != "Z":
        fork = next(trail)
        current = network[current][fork]
        steps += 1

    return steps


def main():
    """finds solution"""

    network = {}

    filename = "./python/2023/input/08.txt"
    lines = []
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]

    path = list(lines[0][:])

    for line in lines[2:]:
        node, left, right = re.findall(r"\w+", line)
        network[node] = {"L": left, "R": right}

    starting = [x for x in network if x[-1] == "A"]
    step_counts = [get_steps(path,x,network) for x in starting]
    total_steps = lcm(*step_counts)

    print_solution(total_steps)

if __name__ == "__main__":
    main()
