def printSolution(x):
    print(f"The solution is: {x}")


class LookSay():
    def __init__(self, start):
        self.sequence = ''

        if len(start) == 0:
            raise ValueError("starting value should be at least one digit")

        self.sequence = start

    def step(self):
        updated = ''
        counter = 1
        if len(self.sequence) == 1:
            updated = str(counter) + self.sequence
        else:
            for idx, digit in enumerate(self.sequence[1:]):
                if digit == self.sequence[idx]:
                    counter += 1
                else:
                    updated += str(counter) + self.sequence[idx]
                    counter = 1
            updated += str(counter) + self.sequence[-1]

        self.sequence = updated


def main():
    input = '1321131112'
    turns = 40

    game = LookSay(input)
    for i in range(1, turns + 1):
        game.step()

    printSolution(len(game.sequence))


if __name__ == "__main__":
    main()
