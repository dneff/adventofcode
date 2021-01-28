def printSolution(x):
    print(f"The solution is: {x}")


def isTriangle(x, y, z):
    longest = max(x, y, z)
    other_two = sum([x, y, z]) - longest
    return longest < other_two


def main():

    file = open("input.txt", "r")
    triangle_count = 0
    for line in file:
        sides = [int(x) for x in line.split()]
        if isTriangle(*sides):
            triangle_count += 1
    printSolution(triangle_count)


if __name__ == "__main__":
    main()
