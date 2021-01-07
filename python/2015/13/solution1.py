from collections import defaultdict
from itertools import permutations


def printSolution(x):
    print(f"The solution is: {x}")


def main():

    file = open("input.txt", "r")

    happiness = defaultdict(dict)

    for line in file:
        line = line.strip().strip(".")
        if "would lose" in line:
            line = line.replace("would lose ", "-").split()
        else:
            line = line.replace("would gain ", "").split()
        subject, difference, guest = line[0], int(line[1]), line[-1]

        happiness[subject][guest] = difference

    most_happy = 0
    for seating in permutations(happiness.keys()):
        table_happiness = sum([happiness[x][y] + happiness[y][x] for x, y in zip(seating, seating[1:])])
        table_happiness += happiness[seating[0]][seating[-1]] + happiness[seating[-1]][seating[0]]
        most_happy = max(most_happy, table_happiness)

    printSolution(most_happy)


if __name__ == "__main__":
    main()
