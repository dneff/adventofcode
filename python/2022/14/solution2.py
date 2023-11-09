def print_solution(x):
    """
    print value passed as solution
    """
    print(f"The solution is {x}")


def generate_cave(file):
    """
    take input file and generate map
    return dict of locations
    """
    cave = {}
    rock = "#"
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            locations = line.strip().split(" -> ")
            locations = [
                (int(x.split(",")[0]), int(x.split(",")[1])) for x in locations
            ]
            for idx in range(len(locations) - 1):
                start, end = locations[idx], locations[idx + 1]
                if start[0] == end[0]:
                    x = start[0]
                    for y in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
                        cave[(x, y)] = rock
                else:
                    y = start[1]
                    for x in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
                        cave[(x, y)] = rock

    return cave


def add_sand(cave, depth):
    # add a grain of sand to the cave
    # return true if sand can be added
    # return false if sand is blocked from entering

    fill_point = (500, 0)
    pos = fill_point

    while pos[1] < depth:
        new_depth = pos[1] + 1
        left, middle, right = (
            (pos[0] - 1, new_depth),
            (pos[0], new_depth),
            (pos[0] + 1, new_depth),
        )
        if middle not in cave.keys():
            pos = middle
        elif left not in cave.keys():
            pos = left
        elif right not in cave.keys():
            pos = right
        else:
            cave[pos] = "o"
            # can't add more sand
            if pos == fill_point:
                return False
            return True
    # on the floor of cave
    cave[pos] = "o"
    return True


def print_cave(cave):
    max_depth = max([x[1] for x in cave.keys()])
    left = min([x[0] for x in cave.keys()])
    right = max([x[0] for x in cave.keys()])
    grid = []
    for y in range(0, max_depth + 1):
        scan = ""
        for x in range(left, right + 1):
            if (x, y) in cave:
                scan += cave[(x, y)]
            else:
                scan += "."
        grid.append(scan)

    for line in grid:
        print(line)


def main():
    file = "../input/14.txt"
    cave = generate_cave(file)
    # floor is two lower than max rock depth
    floor = max([x[1] for x in cave.keys()]) + 2

    filling = True
    while filling:
        filling = add_sand(cave, floor - 1)

    resting_sand = sum([1 for x in cave.values() if x != "#"])

    print_solution(resting_sand)
    print_cave(cave)


if __name__ == "__main__":
    main()
