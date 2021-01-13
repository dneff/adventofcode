from collections import defaultdict


def printSolution(x):
    print(f"The solution is: {x}")


class Display:
    def __init__(self):
        self.lights = {}
        self.step = 0
        self.width = 0

    def add(self, light):
        self.lights[light] = True

    def getNeighbors(self, point):
        neighbors = []
        offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for offset in offsets:
            possible = tuple(map(sum, zip(point, offset)))
            if max((possible)) > self.width or min(possible) < 0:
                continue
            neighbors.append(possible)
        return neighbors

    def cycle(self):
        on = []
        neighbors = defaultdict(int)
        for light in self.lights:
            for neighbor in self.getNeighbors(light):
                neighbors[neighbor] += 1
        off = [k for k in self.lights if neighbors[k] not in [2, 3]]
        on = [k for k, v in neighbors.items() if v == 3]
        for light in off:
            self.lights.pop(light)
        for light in on:
            self.lights[light] = True
        self.step += 1

    def display(self):
        grid = []
        for r in range(self.width + 1):
            row = ""
            for c in range(self.width + 1):
                if (r, c) in self.lights:
                    row = row + "#"
                else:
                    row = row + "."
            grid.append(row)
        return ('\n').join(grid)

def main():

    step_count = 100
    xmas_lights = Display()

    file = open("input.txt", "r")
    width = 0
    for row, line in enumerate(file.readlines()):
        for column, char in enumerate(line.strip()):
            if char == "#":
                xmas_lights.add((row, column))
        width = max(width, row)

    xmas_lights.width = width

    while xmas_lights.step < step_count:
        xmas_lights.cycle()

    printSolution(len(xmas_lights.lights))


if __name__ == "__main__":
    main()
