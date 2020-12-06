def printSolution(x):
    print(f"The solution is: {x}")


class Group:
    def __init__(self):
        self.answers = {}

    def __len__(self):
        return len(self.answers.keys())

    def add(self, answer):
        self.answers[answer] = True


def main():

    groups = []
    file = open("input.txt", "r")

    g = Group()
    for line in file:
        if line.strip():
            for a in line.strip():
                g.add(a)
        else:
            groups.append(g)
            g = Group()

    groups.append(g)

    printSolution(sum([len(x) for x in groups]))


if __name__ == "__main__":
    main()