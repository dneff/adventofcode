from collections import defaultdict


def printSolution(x):
    print(f"The solution is: {x}")


def main():

    file = open("input.txt", "r")
    path = file.readline().strip()

    move = {"^": (0, 1), ">": (1, 0), "v": (0, -1), "<": (-1, 0)}

    houses = defaultdict(int)

    location = (0, 0)
    houses[location] += 1

    for house in path:
        location = tuple([x+y for x, y in zip(location, move[house])])
        houses[location] += 1

    printSolution(len(houses.keys()))


if __name__ == "__main__":
    main()
