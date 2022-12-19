from collections import defaultdict


def printSolution(x):
    print(f"The solution is {x}")


def getDigits(signals):
    result = []
    for digit in signals:
        if len(digit) == 2:
            result.append(1)
        elif len(digit) == 3:
            result.append(7)
        elif len(digit) == 4:
            result.append(4)
        elif len(digit) == 7:
            result.append(8)
    return result


def main():
    test = 'test.txt'
    puzzle = 'input.txt'
    active = puzzle
    file = open(active, 'r')
    easy_digit_count = 0
    for line in file.readlines():
        pattern, output = line.strip().split('|')
        pattern, output = pattern.split(), output.split()
        easy_digit_count += len(getDigits(output))

    printSolution(easy_digit_count)


if __name__ == "__main__":
    main()
