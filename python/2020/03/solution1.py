def printSolution(x):
    print(f"The solution is: {x}")


def main():
    file = open("test_input.txt", "r")

    for line in file:
        l = line.strip()
        if l[x % len(l)] == "#":
            treeCount += 1
        x += 3

    printSolution(treeCount)


if __name__ == "__main__":
    main()
