def printSolution(x):
    print(f"The solution is: {x}")


class Keypad:
    def __init__(self):
        self.position = (0, 2)
        self.keys = {
            (2, 0): "1",
            (1, 1): "2",
            (2, 1): "3",
            (3, 1): "4",
            (0, 2): "5",
            (1, 2): "6",
            (2, 2): "7",
            (3, 2): "8",
            (4, 2): "9",
            (1, 3): "A",
            (2, 3): "B",
            (3, 3): "C",
            (2, 4): "D",
        }

    def move(self, direction):
        self.offsets = {"U": (0, -1), "R": (1, 0), "D": (0, 1), "L": (-1, 0)}
        delta = self.offsets[direction]
        new_position = tuple([x + y for x, y in zip(self.position, delta)])
        if new_position in self.keys:
            self.position = new_position

    def getPosition(self):
        return self.keys[self.position]

    def reset(self):
        self.position = (1, 1)


def main():
    file = open("input.txt", "r")

    bathroom = Keypad()

    code = ""
    for sequence in file:
        for direction in sequence.strip():
            bathroom.move(direction)

        code += bathroom.getPosition()

    printSolution(code)


if __name__ == "__main__":
    main()