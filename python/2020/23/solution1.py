def printSolution(x):
    print(f"The solution is: {x}")


class CrabCups:
    def __init__(self, data):
        self.move = 0
        self.cups = []
        self.held = []
        self.current = 0
        self.cups.extend(data)

    def playMove(self):
        self.move += 1
        current_label = self.cups[self.current]
        pull_idx = (self.current + 1) % len(self.cups)
        for _ in range(3):
            try:
                self.held.append(self.cups.pop(pull_idx))
            except IndexError:
                self.held.append(self.cups.pop(0))
        destination = self.getDestination(current_label)
        insert = self.cups.index(destination) + 1
        while self.held:
            self.cups.insert(insert, self.held.pop())
        # realign the array so current_label is in self.current location
        while self.cups.index(current_label) != self.current:
            self.rotateCups()

        self.current = (self.current + 1) % len(self.cups)

    def getDestination(self, label):
        destination = label - 1
        if destination == 0:
            destination = len(self.cups) + len(self.held)
        while destination in self.held:
            destination -= 1
            if destination == 0:
                destination = len(self.cups) + len(self.held)
        return destination

    def rotateCups(self):
        self.cups = self.cups[-1:] + self.cups[:-1]

    def __repr__(self):
        return (
            f"CrabCups: move: {self.move}, current: {self.current}, cups: {self.cups}"
        )


def main():
    input = [int(x) for x in "215694783"]

    game = CrabCups(input)

    for i in range(100):
        game.playMove()

    final_cups = game.cups
    start = final_cups.index(1)
    final_cups = final_cups[start:] + final_cups[:start]
    printSolution("".join([str(x) for x in final_cups[1:]]))


if __name__ == "__main__":
    main()
