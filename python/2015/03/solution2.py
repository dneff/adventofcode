from collections import defaultdict


def printSolution(x):
    print(f"The solution is: {x}")


def main():

    file = open("input.txt", "r")
    path = file.readline().strip()

    move = {"^": (0, 1), ">": (1, 0), "v": (0, -1), "<": (-1, 0)}

    houses = defaultdict(int)

    santa_location = (0, 0)
    robo_location = (0, 0)

    locations = [santa_location, robo_location]

    for loc in locations:
        houses[loc] += 1

    for idx, house in enumerate(path):
        turn = idx % 2

        locations[turn] = tuple([x + y for x, y in zip(locations[turn], move[house])])
        houses[locations[turn]] += 1

    printSolution(len(houses.keys()))


if __name__ == "__main__":
    main()
