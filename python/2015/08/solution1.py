def printSolution(x):
    print(f"The solution is: {x}")


def main():

    file = open("input.txt", "r")

    diff = 0
    for line in file:
        line = line.strip()
        processed = bytes(line, "utf-8").decode("unicode_escape")
        if processed[0] == '"':
            processed = processed[1:]
        if processed[-1] == '"':
            processed = processed[:-1]
        diff += len(line) - len(processed)

    printSolution(diff)


if __name__ == "__main__":
    main()
