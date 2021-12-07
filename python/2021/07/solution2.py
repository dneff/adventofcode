import statistics


def printSolution(x):
    print(f"The solution is {x}")


def calculateFuel(distance):
    return sum(range(1, distance+1))


def main():
    file = open('input.txt', 'r')
    data = [int(x) for x in file.readline().strip().split(',')]

    target_position = int(statistics.median(data))
    target_fuel = [calculateFuel(abs(x-y)) for x, y in zip(data, [target_position] * len(data))]

    searching = True
    while searching:
        new_position = target_position + 1
        new_fuel = [calculateFuel(abs(x-y)) for x, y in zip(data, [new_position] * len(data))]
        if sum(new_fuel) > sum(target_fuel):
            searching = False
        else:
            target_fuel = new_fuel
            target_position = new_position


    printSolution(sum(target_fuel))

if __name__ == "__main__":
    main()
