def printSolution(x):
    print(f"The solution is: {x}")


class Keypad:
    def __init__(self):
        self.position = (1, 1)

    def move(self, direction):
        self.offsets = {"U": (0, -1), "R": (1, 0), "D": (0, 1), "L": (-1, 0)}
        delta = self.offsets[direction]
        new_position = tuple([x + y for x, y in zip(self.position, delta)])
        if max(new_position) <= 2 and min(new_position) >= 0:
            self.position = new_position

    def getPosition(self):
        return self.position[0] + 1 + self.position[1] * 3

    def reset(self):
        self.position = (1, 1)


def main():
    file = open("input.txt", "r")

    bathroom = Keypad()

    code = []
    for sequence in file:
        for direction in sequence.strip():
            bathroom.move(direction)


        code.append(bathroom.getPosition())

    code = ''.join([str(x) for x in code])
    printSolution(code)


if __name__ == "__main__":
    main()