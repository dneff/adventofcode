
def printSolution(x):
    print(f"The solution is {x}")

def main():
    test = 5
    puzzle1 = 3004953

    active = puzzle1

    elves = list(range(1, active + 1))

    while len(elves) != 1:
        extra = len(elves) % 2 == 1

        elves = elves[::2]
        if extra:
            elves.pop(0)

    printSolution(elves[0])

if __name__ == "__main__":
    main()