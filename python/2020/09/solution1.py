from collections import deque


def printSolution(x):
    print(f"The solution is: {x}")


def main():
    preamble = 25

    file = open("input.txt", "r")

    queue = deque([], preamble)
    for line in file.readlines():
        if len(queue) < preamble:
            queue.append(int(line.strip()))
            continue

        x = int(line.strip())

        valid = False
        for y in queue:
            if x - y in queue:
                valid = True
                break
        if not valid:
            printSolution(x)
            break
        queue.append(x)


if __name__ == "__main__":
    main()