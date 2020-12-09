from collections import deque


def printSolution(x):
    print(f"The solution is: {x}")


def main():
    preamble = 25
    invalid = 0
    file = open("input.txt", "r")
    data = [int(line.strip()) for line in file.readlines()]

    queue = deque([], preamble)

    for num in data:
        if len(queue) < preamble:
            queue.append(num)
            continue

        valid = False
        for y in queue:
            if num - y in queue:
                valid = True
                break
        if not valid:
            invalid = num
            break
        queue.append(num)

    printSolution(invalid)


if __name__ == "__main__":