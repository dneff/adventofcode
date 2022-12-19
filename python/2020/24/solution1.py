from collections import defaultdict


def printSolution(x):
    print(f"The solution is: {x}")


class Hex:
    def __init__(self):
        self.loc = [0, 0, 0]
        self.offset = {}

        self.offset["ne"] = (1, -1, 0)
        self.offset["e"] = (1, 0, -1)
        self.offset["se"] = (0, 1, -1)
        self.offset["sw"] = (-1, 1, 0)
        self.offset["w"] = (-1, 0, 1)
        self.offset["nw"] = (0, -1, 1)

    def move(self, direction):
        self.loc = [x + y for x, y in zip(self.loc, self.offset[direction])]

    def reset(self):
        self.loc = [0, 0, 0]

    def __repr__(self):
        return f"Hex: loc: {self.loc}"


def main():
    file = open("input.txt", "r")

    locations = defaultdict(int)
    paths = []

    for line in file:
        line = line.strip()
        line = (
            line.replace("ne", " ne ")
            .replace("se", " se ")
            .replace("nw", " nw ")
            .replace("sw", " sw ")
        )
        line = (
            line.replace("ee", " e e ")
            .replace("ww", " w w ")
            .replace("ew", " e w ")
            .replace("we", " w e ")
        )
        paths.append(line.split())

    for path in paths:
        h = Hex()
        for move in path:
            h.move(move)
        locations[tuple(h.loc)] += 1

    printSolution(sum([x % 2 for x in locations.values()]))


if __name__ == "__main__":
    main()
