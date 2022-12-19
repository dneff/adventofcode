import re
from collections import defaultdict


def printSolution(x):
    print(f"The solution is: {x}")


def main():

    replacements = defaultdict(list)
    file = open("input.txt", "r")
    for line in file:
        if not line.strip():
            break
        start, end = line.strip().split(" => ")
        replacements[start].append(end)

    molecule = file.readline().strip()
    created = set()
    for element in replacements:
        element_locs = [loc.span() for loc in re.finditer(element, molecule)]
        for loc in element_locs:
            for substitution in replacements[element]:
                created.add(molecule[:loc[0]] + substitution + molecule[loc[1]:])

    printSolution(len(created))


if __name__ == "__main__":
    main()
