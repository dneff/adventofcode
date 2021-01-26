from itertools import combinations
from functools import reduce

def printSolution(x):
    print(f"The solution is: {x}")


def main():

    file = open("input.txt", "r")
    numbers = [int(x) for x in file.readlines()]
    target = sum(numbers) // 4

    max_len = 1
    while sum(numbers[:max_len]) <= target:
        max_len += 1
    min_len = 1
    while sum(numbers[-min_len:]) <= target:
        min_len += 1

    buckets = set()
    min_combo = len(numbers)
    qe = {}

    for l in range(min_len, max_len + 1):
        combos = combinations(numbers, l)
        for x in combos:
            if sum(x) == target:
                buckets.add(x)
                min_combo = min(min_combo, len(x))
                qe[reduce((lambda a, b: a*b), x)] = x

    print(min(qe))


if __name__ == "__main__":
    main()
