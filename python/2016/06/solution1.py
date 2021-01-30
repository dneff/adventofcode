from collections import defaultdict


def printSolution(x):
    print(f"The solution is: {x}")


def main():
    file = open("input.txt", "r")

    position = [defaultdict(int)] * 8

    for line in file:
        for index, char in enumerate(line.strip()):
            position[index][char] += 1

    for d in position:
        print(sorted(d, key=d.itemgetter(), reverse=True))

if __name__ == "__main__":
    main()
