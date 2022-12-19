
def printSolution(x):
    print(f"The solution is: {x}")


def main():
    file = open('input.txt', 'r')
    valid_count = 0
    for line in file.readlines():
        words = line.strip().split()
        if len(words) == len(set(words)):
            valid_count += 1

    printSolution(valid_count)


if __name__ == "__main__":
    main()
