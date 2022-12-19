import statistics


def printSolution(x):
    print(f"The solution is {x}")


def main():
    file = open('input.txt', 'r')
    data = [int(x) for x in file.readline().strip().split(',')]

    median = int(statistics.median(data))
    fuel = [abs(x-y) for x, y in zip(data, [median] * len(data))]
    print(sum(fuel))


if __name__ == "__main__":
    main()
