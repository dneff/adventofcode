
def printSolution(x):
    print(f"The solution is: {x}")


def main():
    f = open('input.txt', 'r')
    row_minmax = []
    for row in f.readlines():
        r = [int(x) for x in row.split()]
        row_minmax.append(max(r) - min(r))

    printSolution(sum(row_minmax))


if __name__ == "__main__":
    main()
