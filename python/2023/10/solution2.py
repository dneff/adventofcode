"""solves 2023 day 10 part 2"""

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


def get_sides(position, landscape):
    """return all positions to the left and right of the loop"""
    left_locs = []
    right_locs = []
    loop_locs = []
    current = position
    while current not in loop_locs:
        loop_locs.append(current)
        for loc in landscape[current]:
            if loc not in loop_locs:
                current = loc
        # find orientation
        x, y = current
        last_x, last_y = loop_locs[-1][0], loop_locs[-1][1]
        offset = (x - last_x, y - last_y)

        if offset[0] == 0:
            if offset[1] == -1:
                # going up (0,-1)
                left_locs.append((x - 1, y))
                left_locs.append((last_x - 1, last_y))
                right_locs.append((x + 1, y))
                right_locs.append((last_x + 1, last_y))
            else:
                # going down (0,1)
                left_locs.append((x + 1, y))
                left_locs.append((last_x + 1, last_y))
                right_locs.append((x - 1, y))
                right_locs.append((last_x - 1, last_y))
        else:
            if offset[0] == 1:
                # going right (1,0)
                left_locs.append((x, y - 1))
                left_locs.append((last_x, last_y - 1))
                right_locs.append((x, y + 1))
                right_locs.append((last_x, last_y + 1))
            else:
                # going left (-1,0)
                left_locs.append((x, y + 1))
                left_locs.append((last_x, last_y + 1))
                right_locs.append((x, y - 1))
                right_locs.append((last_x, last_y - 1))

    left_locs = list(set([x for x in left_locs if x not in loop_locs]))
    right_locs = list(set([x for x in right_locs if x not in loop_locs]))

    return left_locs, right_locs


def is_edge(pos, edges):
    """is position next to edge?"""
    x, y = pos
    possible = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]
    for loc in possible:
        if loc in edges:
            return True
    return False


def main():
    """loads and solves puzzle"""
    filename = "./python/2023/input/10.txt"

    lines = []
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]

    landscape = {}
    start = (0, 0)
    size = (len(lines[0]), len(lines))

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

    # find loop
    loop = get_loop(start, landscape)

    # flood landscape to find outside edges
    edges = []
    void = []
    for y in range(size[1]):
        for x in range(size[0]):
            if (x, y) in loop:
                continue
            if x in (0, size[0] - 1) or y in (0, size[1] - 1):
                edges.append((x, y))
            else:
                void.append((x, y))

    finding = True
    while finding:
        finding = False
        for pos in void[:]:
            if is_edge(pos, edges):
                edges.append(pos)
                void.pop(void.index(pos))
                finding = True

    # get left and right sides of pipe and figure out which side is "inside"
    left, right = get_sides(start, landscape)
    inside, outside = None, None

    if len(set(edges) & set(left)) > 0:
        inside = right
        outside = left
    else:
        inside = left
        outside = right

    # inside is remaining locs after removing outside locs, edges, and pipe loop
    taken = list(set(loop).union(set(outside), set(edges)))
    inside_locs = 0
    for y in range(size[1]):
        for x in range(size[0]):
            if (x, y) in taken:
                continue
            if (x, y) in inside:
                inside_locs += 1
            else:
                inside_locs += 1

    print_solution(inside_locs)


if __name__ == "__main__":
    main()
