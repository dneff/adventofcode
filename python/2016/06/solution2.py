from collections import defaultdict
from operator import itemgetter


def printSolution(x):
    print(f"The solution is: {x}")


def getMinKey(dict_x):
    ordered_keys = [x for x, y in sorted(dict_x.items(), key=itemgetter(1), reverse=True)]
    return ordered_keys[-1]


def main():
    file = open("input.txt", "r")

    position = []

    for _ in range(8):
        position.append(defaultdict(int))

    for line in file:
        for index, char in enumerate(line.strip()):
            position[index][char] += 1

    message = ""
    for d in position:
        message += getMinKey(d)

    printSolution(message)


if __name__ == "__main__":
    main()
