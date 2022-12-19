def printSolution(x):
    print(f"The solution is: {x}")


class GridBug:
    def __init__(self):
        self.visited = set((0, 0))
        self.directions = ["N", "E", "S", "W"]
        self.location = (0, 0)
        self.orientation = 0
        self.offsets = {"N": (0, 1), "E": (1, 0), "S": (0, -1), "W": (-1, 0)}

    def turn(self, direction):
        if direction == "L":
            self.orientation = (self.orientation - 1) % 4
        elif direction == "R":
            self.orientation = (self.orientation + 1) % 4

    def move(self, distance):
        direction = self.directions[self.orientation]
        for _ in range(distance):
            self.location = tuple([x + y for x, y in zip(self.location, self.offsets[direction])])
            if self.location in self.visited:
                raise ValueError(f"already been here: {self.location}")
            else:
                self.visited.add(self.location)

    def getDistance(self):
        return abs(self.location[0]) + abs(self.location[1])


def main():
    file = open("input.txt", "r")

    sleigh = GridBug()

    instructions = [(x[0], int(x[1:])) for x in file.readline().split(", ")]

    for i in instructions:
        sleigh.turn(i[0])
        try:
            sleigh.move(i[1])
        except ValueError:
            printSolution(sleigh.getDistance())
            break


if __name__ == "__main__":
    main()
