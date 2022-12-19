def printSolution(x):
    print(f"The solution is: {x}")


def nextCode(x):
    if x == 0:
        return 20151125
    else:
        return (x * 252533) % 33554393


def getIterations(row, col):
    max_row = row + col - 1
    iterations = sum([x for x in range(max_row)])
    iterations += col
    return iterations


def main():
    code_loc = (2978, 3083)

    code = 0
    for _ in range(getIterations(*code_loc)):
        code = nextCode(code)

    printSolution(code)


if __name__ == "__main__":
    main()
