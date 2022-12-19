def printSolution(x):
    print(f"The solution is: {x}")


def main():

    file = open("input.txt", "r")
    data = [0]  # outlet
    data.extend([int(line.strip()) for line in file.readlines()])
    data.sort()
    data.append(max(data) + 3)  # device

    differences = [y - x for x, y in zip(data, data[1:])]

    printSolution(differences.count(1) * differences.count(3))


if __name__ == "__main__":
    main()