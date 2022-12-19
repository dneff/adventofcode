import copy


def printSolution(x):
    print(f"The solution is {x}")


def main():
    test = 'test.txt'
    puzzle = 'input.txt'

    file = open(puzzle, 'r')
    chart = [x.strip() for x in file.readlines()]

    east = set()
    south = set()

    max_x = len(chart[0])
    max_y = len(chart)

    for y, row in enumerate(chart):
        for x, loc in enumerate(row):
            if loc == '>':
                east.add((x, y))
            elif loc == 'v':
                south.add((x, y))

    steps = 0
    moving = True
    while moving:
        starting = east | south

        new_east = set()
        for cuke in east:
            x, y = cuke
            moved = ((x + 1) % max_x, y)
            if moved not in starting:
                new_east.add(moved)
            else:
                new_east.add(cuke)

        mid = new_east | south

        new_south = set()
        for cuke in south:
            x, y = cuke
            moved = (x, (y + 1) % max_y)
            if moved not in mid:
                new_south.add(moved)
            else:
                new_south.add(cuke)

        ending = new_east | new_south
        steps += 1
        if starting == ending:
            moving = False
        else:
            east, south = copy.deepcopy(new_east), copy.deepcopy(new_south)

    printSolution(steps)


if __name__ == "__main__":
    main()
