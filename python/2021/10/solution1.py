
from collections import deque


def printSolution(x):
    print(f"The solution is {x}")


class Checker():

    def __init__(self):
        self.stack = deque()
        self.score = {
            ')': 3,
            ']': 57,
            '}': 1197,
            '>': 25137
        }
        self.match = {
            ')': '(',
            ']': '[',
            '}': '{',
            '>': '<'
        }

    def parse(self, data):
        for symbol in data:
            if symbol not in self.match.keys():
                self.stack.append(symbol)
            else:
                stack_symbol = self.stack.pop()
                if self.match[symbol] != stack_symbol:
                    return self.score[symbol]
        return 0


def main():
    test = 'test.txt'
    puzzle = 'input.txt'

    parser = Checker()

    file = open(puzzle, 'r')
    line_values = []
    for line in file.readlines():
        line_values.append(parser.parse(line.strip()))

    printSolution(sum(line_values))
        


if __name__ == "__main__":
    main()
