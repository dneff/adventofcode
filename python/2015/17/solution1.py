
def printSolution(x):
    print(f"The solution is: {x}")


def main():

    eggnog = 150

    file = open("input.txt", "r")
    containers = [int(x) for x in file.readlines()]

    valid_combos = 0

    for x in range(1, 2 ** len(containers)):
        mask = str(bin(x))[2:].zfill(len(containers))
        mask = [int(x) for x in mask]
        container_value = sum(x * y for x, y in zip(mask, containers))

        if container_value == eggnog:
            valid_combos += 1

    printSolution(valid_combos)


if __name__ == "__main__":
    main()
