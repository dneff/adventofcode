from collections import defaultdict


def printSolution(x):
    print(f"The solution is: {x}")


def main():
    file = open("input.txt", "r")
    time = int(file.readline().strip())
    buses = [int(x) for x in file.readline().split(",") if x != "x"]

    eta = defaultdict(list)
    for bus in buses:
        eta[bus - time % bus].append(bus)

    earliest_time = min(eta.keys())
    printSolution(earliest_time * eta[earliest_time][0])


if __name__ == "__main__":
    main()