from itertools import permutations


def printSolution(x):
    print(f"The solution is: {x}")


def main():

    cities = {}

    file = open("input.txt", "r")

    for line in file:
        c1c2, distance = line.strip().split(" = ")
        c1, c2 = c1c2.split(" to ")
        distance = int(distance)
        for city in [c1, c2]:
            if city not in cities:
                cities[city] = {}
        cities[c1][c2] = distance
        cities[c2][c1] = distance

    shortest = 0
    for x in permutations(cities.keys(), len(cities.keys())):
        route = [cities[x][y] for x, y in zip(x[:], x[1:])]
        if shortest == 0:
            shortest = sum(route)
        else:
            shortest = min(shortest, sum(route))

    printSolution(shortest)


if __name__ == "__main__":
    main()
