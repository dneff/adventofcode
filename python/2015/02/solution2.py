def printSolution(x):
    print(f"The solution is: {x}")


def getWrapping(length, width, height):
    sides = [length * width, width * height, height * length]
    wrapping = 2 * sum(sides)
    slack = min(sides)
    return wrapping + slack


def getRibbon(length, width, height):
    sides = [length + width, width + height, height + length]
    ribbon = 2 * min(sides)
    return ribbon


def getBow(length, width, height):
    bow = length * width * height
    return bow


def main():

    file = open("input.txt", "r")

    total_ribbon = 0
    for line in file:
        l, w, h = [int(x) for x in line.strip().split("x")]
        total_ribbon += getRibbon(l, w, h)
        total_ribbon += getBow(l, w, h)

    printSolution(total_ribbon)


if __name__ == "__main__":
    main()
