from collections import defaultdict


def printSolution(x):
    print(f"The solution is {x}")


class Reactor:
    def __init__(self):
        self.reactor = defaultdict(int)

    def on(self, position):
        self.reactor[position] = 1

    def off(self, position):
        try:
            self.reactor.pop(position)
        except KeyError:
            pass

    def getCoreCount(self):
        counter = 0
        for k, v in self.reactor.items():
            if all([-50 <= x <= 50 for x in k]):
                counter += v
        return counter


def main():
    test = 'test.txt'
    puzzle = 'input.txt'

    reactor = Reactor()

    file = open(puzzle, 'r')
    for line in file.readlines():
        command, positions = line.strip().split()
        command = getattr(reactor, command)
        x, y, z = positions.split(',')
        x = [int(x) for x in x.split('=')[-1].split('..')]
        y = [int(y) for y in y.split('=')[-1].split('..')]
        z = [int(z) for z in z.split('=')[-1].split('..')]
        for p_x in range(max(min(x), -50), min(max(x), 50)+1):
            for p_y in range(max(min(y), -50), min(max(y), 50)+1):
                for p_z in range(max(min(z), -50), min(max(z), 50)+1):
                    command((p_x, p_y, p_z))

    printSolution(reactor.getCoreCount())


if __name__ == "__main__":
    main()
