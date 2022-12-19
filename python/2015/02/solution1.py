def printSolution(x):
    print(f"The solution is: {x}")


def getWrapping(length, width, height):
    sides = [length * width, width * height, height * length]
    wrapping = 2 * sum(sides)
    slack = min(sides)
    return wrapping + slack


def main():

    file = open("input.txt", "r")

    total_wrapping = 0
    for line in file:
        l, w, h = [int(x) for x in line.strip().split("x")]
        total_wrapping += getWrapping(l, w, h)

    printSolution(total_wrapping)


if __name__ == "__main__":
    main()
