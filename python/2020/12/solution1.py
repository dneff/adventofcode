def printSolution(x):
    print(f"The solution is: {x}")


class Boat:
    def __init__(self):
        self.compass = ["N", "E", "S", "W"]
        self.heading = 1
        self.position = (0, 0)

    def N(self, distance):
        self.position = (self.position[0], self.position[1] + distance)

    def S(self, distance):
        self.position = (self.position[0], self.position[1] - distance)

    def E(self, distance):
        self.position = (self.position[0] + distance, self.position[1])

    def W(self, distance):
        self.position = (self.position[0] - distance, self.position[1])

    def L(self, degrees):
        turn = degrees // 90
        self.heading = (self.heading - turn) % 4

    def R(self, degrees):
        turn = degrees // 90
        self.heading = (self.heading + turn) % 4

    def F(self, distance):
        direction = getattr(self, self.compass[self.heading])
        return direction(distance)


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