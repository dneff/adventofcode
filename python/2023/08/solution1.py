"""solution to 2023 Day 8 solution 1"""
import re


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

    trail = get_next(path)
    current = "AAA"
    steps = 0

    while current != "ZZZ":
        fork = next(trail)
        current = network[current][fork]
        steps += 1

    print_solution(steps)


if __name__ == "__main__":
    main()
