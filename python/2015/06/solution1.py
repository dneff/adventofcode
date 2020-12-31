from collections import defaultdict


def printSolution(x):
    print(f"The solution is: {x}")


class Lights:
    def __init__(self):
        self.grid = defaultdict(int)

    def on(self, start, end):
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.grid[(row, column)] = 1

    def off(self, start, end):
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.grid[(row, column)] = 0

    def toggle(self, start, end):
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.grid[(row, column)] = (self.grid[(row, column)] + 1) % 2

    def lit(self):
        return sum(self.grid.values())


def main():

    file = open("input.txt", "r")

    display = Lights()

    for line in file:
        line = line.strip()
        line = line.replace("turn on", "on").replace("turn off", "off").replace("through", "")
        action, start, end = line.split()
        start = tuple([int(x) for x in start.split(",")])
        end = tuple([int(x) for x in end.split(",")])

        getattr(display, action)(start, end)

    printSolution(display.lit())


if __name__ == "__main__":
    main()
