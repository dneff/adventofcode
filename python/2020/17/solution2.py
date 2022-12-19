from collections import defaultdict


def printSolution(x):
    print(f"The solution is: {x}")


class ConwayCube:
    def __init__(self, cube_data):
        self.cycles = 0
        self.pocket = {}

        row = 0
        for line in cube_data:
            for column, cube in enumerate(line):
                if cube == "#":
                    self.pocket[(row, column, 0, 0)] = True
            row += 1

    def cycle(self):
        self.cycles += 1

        to_activate = defaultdict(int)
        to_deactivate = []
        for cube in self.pocket.keys():
            neighbors = self.getAdjacent(cube)
            neighbor_count = 0
            # find positions to activate
            for position in neighbors:
                if position in self.pocket.keys():
                    neighbor_count += 1
                else:
                    to_activate[position] += 1
            if neighbor_count not in [2, 3]:
                to_deactivate.append(cube)

        # update pocket
        for cube in to_deactivate:
            self.pocket.pop(cube)
        for position, count in to_activate.items():
            if count == 3:
                self.pocket[position] = True

    def getAdjacent(self, cube):
        adjacents = []
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                for z in [-1, 0, 1]:
                    for w in [-1, 0, 1]:
                        if x == y == z == w == 0:
                            continue
                        adjacents.append(
                            tuple([sum(x) for x in zip(cube, (x, y, z, w))])
                        )
        return adjacents

    def start(self, cycle_count=6):
        for x in range(cycle_count):
            self.cycle()

    def cubeCount(self):
        return len(self.pocket.keys())


def main():
    file = open("input.txt", "r")

    cube_data = [line.strip() for line in file]

    engine = ConwayCube(cube_data)

    engine.start()

    printSolution(engine.cubeCount())


if __name__ == "__main__":
    main()
