def printSolution(x):
    print(f"The solution is: {x}")


class CrabCups:
    def __init__(self, data):
        self.move = 0
        self.cups = []
        self.cup_count = 0
        self.next_cup = {}
        self.held = []
        self.current = 0

        self.cups.extend(data)
        self.cup_count = len(self.cups)
        cup_next = self.cups[1:] + self.cups[:1]
        self.next_cup = {cup: cup_n for cup, cup_n in zip(self.cups, cup_next)}
        self.current = self.cups[0]

    def playMove(self):
        self.move += 1

        c1 = self.next_cup[self.current]
        c2 = self.next_cup[c1]
        c3 = self.next_cup[c2]

        destination = self.getDestination([c1, c2, c3])

        self.next_cup[self.current] = self.next_cup[c3]
        self.next_cup[c3] = self.next_cup[destination]
        self.next_cup[destination] = c1

        self.current = self.next_cup[self.current]

    def getDestination(self, held):
        destination = self.current - 1 if self.current > 1 else self.cup_count
        while destination in held:
            destination = destination - 1 if destination > 1 else self.cup_count
        return destination

    def __repr__(self):
        return (
            f"CrabCups: move: {self.move}, current: {self.current}, cups: {self.cups}"
        )


def main():
    input = [int(x) for x in "215694783"]

    for i in range(10, 1000001):
        input.append(i)

    game = CrabCups(input)

    for i in range(10000000):
        game.playMove()
        if i % 100000 == 0:
            print(f"@{i}/10000000")

    first_cup = game.next_cup[1]
    second_cup = game.next_cup[first_cup]
    printSolution(first_cup * second_cup)


if __name__ == "__main__":
    main()
