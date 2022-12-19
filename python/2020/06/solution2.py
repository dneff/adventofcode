from collections import defaultdict


def printSolution(x):
    print(f"The solution is: {x}")


class Group:
    def __init__(self):
        self.answers = defaultdict(int)
        self.members = 0

    def __len__(self):
        return len(self.answers.keys())

    def add(self, answer):
        self.answers[answer] += 1

    def everyone(self):
        allMatched = [v == self.members for v in self.answers.values()]
        return allMatched.count(True)


def main():

    groups = []
    file = open("input.txt", "r")

    g = Group()
    for line in file:
        if line.strip():
            g.members += 1
            for a in line.strip():
                g.add(a)
        else:
            groups.append(g)
            g = Group()

    groups.append(g)

    printSolution(sum([x.everyone() for x in groups]))


if __name__ == "__main__":
    main()