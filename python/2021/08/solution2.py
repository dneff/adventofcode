from collections import defaultdict


def printSolution(x):
    print(f"The solution is {x}")


def getDigits(signals):
    rosetta = defaultdict(set)
    to_decode = [set(list(x)) for x in signals]
    for i, digit in enumerate(to_decode):
        if len(digit) == 2:
            rosetta[1] = digit
        elif len(digit) == 3:
            rosetta[7] = digit
        elif len(digit) == 4:
            rosetta[4] = digit
        elif len(digit) == 7:
            rosetta[8] = digit

    # solve for len == 6 (0, 6, 9)
    for i, digit in enumerate(to_decode):
        if len(digit) == 6:
            if rosetta[8].difference(digit).issubset(rosetta[1]):
                rosetta[6] = digit
            elif rosetta[8].difference(digit).issubset(rosetta[4]):
                rosetta[0] = digit
            else:
                rosetta[9] = digit

    # remainder is len == 5 (2, 3, 5)
    for i, digit in enumerate(to_decode):
        if len(digit) == 5:
            if rosetta[8].difference(rosetta[9]).issubset(digit):
                rosetta[2] = digit
            elif rosetta[8].difference(rosetta[6]).issubset(digit):
                rosetta[3] = digit
            else:
                rosetta[5] = digit

    result = {''.join(sorted(list(v))): k for k, v in rosetta.items()}
    return result


def main():
    test = 'test.txt'
    puzzle = 'input.txt'
    active = puzzle
    file = open(active, 'r')
    output_sum = 0
    for line in file.readlines():
        pattern, output = line.strip().split('|')
        pattern, output = pattern.split(), output.split()
        wiring = getDigits(pattern)
        output_value = ''
        for o in output:
            o = ''.join(sorted(list(o)))
            output_value += str(wiring[o])
        output_sum += int(output_value)

    printSolution(output_sum)


if __name__ == "__main__":
    main()
