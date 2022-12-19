def printSolution(x):
    print(f"The solution is: {x}")


def memoryGame(start, iterations):
    spoken = {}
    time = 1
    curr = start.pop(0)

    while time < iterations:
        if curr not in spoken.keys():
            spoken[curr] = time
            if len(start):
                curr = start.pop(0)
            else:
                curr = 0
        else:
            next = time - spoken[curr]
            spoken[curr] = time
            curr = next
        time += 1

    return curr


def tests():
    tests = {
        1: [1, 3, 2],
        10: [2, 1, 3],
        27: [1, 2, 3],
        78: [2, 3, 1],
        438: [3, 2, 1],
        1836: [3, 1, 2],
    }

    for k, v in tests.items():
        r = memoryGame(v[:], 2020)
        assert k == r


def main():

    puzzle = [9, 19, 1, 6, 0, 5, 4]

    tests()

    printSolution(memoryGame(puzzle, 2020))


if __name__ == "__main__":
    main()