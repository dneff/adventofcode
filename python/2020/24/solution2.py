from collections import defaultdict


def printSolution(x):
    print(f"The solution is: {x}")


class Hex:
    def __init__(self):
        self.loc = (0, 0, 0)
        self.offset = {}

        self.offset["ne"] = (1, -1, 0)
        self.offset["e"] = (1, 0, -1)
        self.offset["se"] = (0, 1, -1)
        self.offset["sw"] = (-1, 1, 0)
        self.offset["w"] = (-1, 0, 1)
        self.offset["nw"] = (0, -1, 1)

    def move(self, direction):
        self.loc = tuple([x + y for x, y in zip(self.loc, self.offset[direction])])

    def findAdjacent(self):
        adj = []
        for o in self.offset.values():
            pos = tuple([x + y for x, y in zip(self.loc, o)])
            adj.append(pos)
        return adj

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

    # remove white tiles from map
    remove = []
    for k, v in locations.items():
        if v % 2 == 0:
            remove.append(k)

    while remove:
        locations.pop(remove.pop())

    days = 100
    for day in range(1, days + 1):

        neighbor_count = defaultdict(int)

        for position in locations:
            h = Hex()
            h.loc = position
            for pos in h.findAdjacent():
                neighbor_count[pos] += 1

        to_add = []
        to_remove = []

        for tile, count in neighbor_count.items():
            if tile not in locations:
                if count == 2:
                    to_add.append(tile)

        for tile in locations.keys():
            if neighbor_count[tile] == 0 or neighbor_count[tile] > 2:
                to_remove.append(tile)

        while to_add:
            locations[to_add.pop()] += 1

        while to_remove:
            locations.pop(to_remove.pop())

        # print(f"Day {day}: {len(locations)}")

    printSolution(len(locations))


if __name__ == "__main__":
    main()
