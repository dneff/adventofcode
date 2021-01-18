def printSolution(x):
    print(f"The solution is: {x}")


def getFactors(x):
    results = []
    for i in range(1, int(x ** 0.5) + 1):
        if x % i == 0:
            results.extend([i, x // i])
    return list(set(results))


def main():

    target_presents = 36000000
    house_number = 0

    delivering = True

    while delivering:
        house_number += 1
        visiting_elves = [elf for elf in getFactors(house_number) if house_number // elf <= 50]
        presents_delivered = sum([11 * elf for elf in visiting_elves])
        delivering = presents_delivered <= target_presents

    printSolution(house_number)


if __name__ == "__main__":
    main()
