def printSolution(x):
    print(f"The solution is: {x}")


def getTribonacciSeries(x):
    seq = [0] * x
    seq[0] = seq[1] = 0
    seq[2] = 1
    for i in range(3, x):
        seq[i] = sum(seq[i - 3 :])
    return seq


def main():

    file = open("input.txt", "r")
    data = [0]  # outlet
    data.extend([int(line.strip()) for line in file.readlines()])
    data.sort()
    data.append(max(data) + 3)  # device

    differences = [y - x for x, y in zip(data, data[1:])]

    s = getTribonacciSeries(10)
    combo_lookup = s[2:]

    combinations = 1
    sequence_size = 0
    for x in differences:
        if x == 1:
            sequence_size += 1
        if x == 3 and sequence_size != 0:
            combinations *= combo_lookup[sequence_size]
            sequence_size = 0

    printSolution(combinations)


if __name__ == "__main__":
    main()