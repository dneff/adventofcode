
def printSolution(x):
    print(f"The solution is: {x}")


def main():
    file = open('input.txt', 'r')
    instructions = [int(value) for value in file.readlines()]

    step = 0
    offset = 0
    while 0 <= offset <= (len(instructions) - 1):
        step += 1
        delta = instructions[offset]
        instructions[offset] += 1
        offset += delta

    printSolution(step)


if __name__ == "__main__":
    main()
