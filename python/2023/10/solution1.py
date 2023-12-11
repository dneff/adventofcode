"""solves 2023 day 10 part 1"""

pipes = {
    "|": [(0, 1), (0, -1)],
    "-": [(-1, 0), (1, 0)],
    "L": [(0, -1), (1, 0)],
    "J": [(-1, 0), (0, -1)],
    "7": [(-1, 0), (0, 1)],
    "F": [(1, 0), (0, 1)],
}


def print_solution(x):
    """output solution"""
    print(f"The solution is: {x}")


def get_adjacent(position, pipe):
    """find adjacent positions based on pipe"""
    p_x, p_y = position
    return [(p_x + x, p_y + y) for x, y in pipes[pipe]]


def get_loop(position, landscape):
    """return all positions in loop"""
    locs = []
    current = position
    while current not in locs:
        locs.append(current)
        for loc in landscape[current]:
            if loc not in locs:
                current = loc
    return locs


def main():
    """loads and solves puzzle"""
    filename = "./python/2023/input/10.txt"

    lines = []
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]

    landscape = {}
    start = (0, 0)
    for y, line in enumerate(lines):
        for x, pipe in enumerate(line):
            if pipe == ".":
                continue
            if pipe == "S":
                start = (x, y)
                continue
            landscape[(x, y)] = get_adjacent((x, y), pipe)

    # attach start
    landscape[start] = [pos for pos, adj in landscape.items() if start in adj]

    loop = get_loop(start, landscape)
    # furthest position is half the loop
    print_solution(len(loop) // 2)


if __name__ == "__main__":
    main()
