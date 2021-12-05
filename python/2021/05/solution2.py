from collections import defaultdict

def printSolution(x):
    print(f"The solution is {x}")


def main():
    puzzle = 'input.txt'
    test = 'test.txt'
    file = open(puzzle, 'r')

    vents = defaultdict(int)

    for line in file.readlines():
        start, end = line.strip().split(' -> ')
        start_x, start_y = [int(x) for x in start.split(',')]
        end_x, end_y = [int(x) for x in end.split(',')]

        if start_x == end_x:
            for y in range(min(start_y, end_y), max(start_y, end_y) + 1):
                vents[(start_x, y)] += 1

        elif start_y == end_y:
            for x in range(min(start_x, end_x), max(start_x, end_x) + 1):
                vents[(x, start_y)] += 1

        elif abs(start_x - end_x) == abs(start_y - end_y):
            end_pos = (end_x, end_y)

            iterator_x = 1
            iterator_y = 1
            if start_x > end_x:
                iterator_x = -1
            if start_y > end_y:
                iterator_y = -1

            position = (start_x, start_y)
            vents[position] += 1

            while position != end_pos:
                position = (position[0] + iterator_x, position[1] + iterator_y)
                vents[position] += 1

    overlaps = sum([1 for x in vents.values() if x > 1])
    printSolution(overlaps)


if __name__ == "__main__":
    main()
