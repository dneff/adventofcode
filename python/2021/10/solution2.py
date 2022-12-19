
from collections import deque


def printSolution(x):
    print(f"The solution is {x}")


class Checker():

    def __init__(self):
        self.stack = deque()
        self.score = {
            ')': 1,
            ']': 2,
            '}': 3,
            '>': 4
        }
        self.match = {
            ')': '(',
            ']': '[',
            '}': '{',
            '>': '<'
        }

    def autocomplete(self, data):
        for symbol in data:
            if symbol not in self.match.keys():
                self.stack.append(symbol)
            else:
                stack_symbol = self.stack.pop()
                if self.match[symbol] != stack_symbol:
                    self.stack.clear()
                    return 0

        return self.heapScore()

    def heapScore(self):
        parse = {v: k for k, v in self.match.items()}
        score = 0
        while len(self.stack) > 0:
            symbol = self.stack.pop()
            score *= 5
            score += self.score[parse[symbol]]
        return score


def main():
    test = 'test.txt'
    puzzle = 'input.txt'

    parser = Checker()

    file = open(puzzle, 'r')
    line_values = []
    for line in file.readlines():
        lv = parser.autocomplete(line.strip())
        if lv != 0:
            line_values.append(lv)

    line_values.sort()
    mid = len(line_values)//2
    printSolution(line_values[mid])


if __name__ == "__main__":
    main()
