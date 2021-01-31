
def printSolution(x):
    print(f"The solution is: {x}")


class cardReader():
    def __init__(self):
        self.height = 6
        self.width = 50
        self.screen = []
        for _ in range(self.height):
            row = ['.'] * self.width
            self.screen.append(row)

    def rect(self, w, h):
        pass

    def rotateColumn(self, column, count):
        pass

    def rotateRow(self, row, count):
        pass

    def litCount(self):
        return sum([row.count('#') for row in self.screen])


def main():

    door = cardReader()

    file = open('input.txt', 'r')
    for line in file:
        print(line.strip())


if __name__ == '__main__':
    main()
