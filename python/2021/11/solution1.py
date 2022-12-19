
def printSolution(x):
    print(f"The solution is {x}")


class OctopusGarden:
    def __init__(self, data):
        self.garden = {}
        self.turn = 0
        self.flash_count = 0
        self.max_r = len(data)
        self.max_c = len(data[0])

        r = 0
        for octos in data:
            for c, octo in enumerate(octos):
                self.garden[(r, c)] = int(octo)
            r += 1

    def getNeighbors(self, position):
        neighbors = [(0, -1), (1, 0), (0, 1), (-1, 0), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        neighbor_positions = []
        for offset in neighbors:
            neighbor_positions.append(tuple([item1 + item2 for item1, item2 in zip(offset, position)]))
        valid = [p for p in neighbor_positions if p in self.garden.keys()]
        return valid

    def step(self):
        for octo in self.garden.keys():
            self.garden[octo] += 1
        flashing_octs = [p for p, o in self.garden.items() if o > 9]
        while len(flashing_octs) > 0:
            for position in flashing_octs:
                self.garden[position] = 0
                self.flash_count += 1
                for n in self.getNeighbors(position):
                    if self.garden[n] != 0:
                        self.garden[n] += 1
            flashing_octs = [p for p, o in self.garden.items() if o > 9]
        self.turn += 1


def main():
    test = 'test.txt'
    puzzle = 'input.txt'

    file = open(puzzle, 'r')
    data = [line.strip() for line in file.readlines()]

    og = OctopusGarden(data)
    for _ in range(100):
        og.step()

    printSolution(og.flash_count)


if __name__ == "__main__":
    main()
