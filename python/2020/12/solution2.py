def printSolution(x):
    print(f"The solution is: {x}")


class Boat:
    def __init__(self):
        self.waypoint = (10, 1)
        self.position = (0, 0)

    def N(self, distance):
        self.waypoint = (self.waypoint[0], self.waypoint[1] + distance)

    def S(self, distance):
        self.waypoint = (self.waypoint[0], self.waypoint[1] - distance)

    def E(self, distance):
        self.waypoint = (self.waypoint[0] + distance, self.waypoint[1])

    def W(self, distance):
        self.waypoint = (self.waypoint[0] - distance, self.waypoint[1])

    def L(self, degrees):
        turn = (degrees // 90) % 4
        x, y = self.waypoint
        if turn % 2 == 1:
            x, y = y, x
        if turn in [1, 2]:
            x *= -1
        if turn in [2, 3]:
            y *= -1
        self.waypoint = (x, y)

    def R(self, degrees):
        turn = (degrees // 90) % 4
        x, y = self.waypoint
        if turn % 2 == 1:
            x, y = y, x
        if turn in [1, 2]:
            y *= -1
        if turn in [2, 3]:
            x *= -1
        self.waypoint = (x, y)

    def F(self, distance):
        x = self.position[0] + self.waypoint[0] * distance
        y = self.position[1] + self.waypoint[1] * distance
        self.position = (x, y)


def main():
    file = open("input.txt", "r")

    ferry = Boat()
    for line in file.readlines():
        l = line.strip()
        i, d = l[0], int(l[1:])
        inst = getattr(ferry, i)
        inst(d)

    printSolution(abs(ferry.position[0]) + abs(ferry.position[1]))


if __name__ == "__main__":
    main()