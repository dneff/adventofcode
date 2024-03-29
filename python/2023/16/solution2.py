"""solves day 16 problem 2"""


def print_solution(x):
    """prints solution"""
    print(f"The solution is:{x}")


direction = {"north": (0, -1), "east": (1, 0), "south": (0, 1), "west": (-1, 0)}


def beam_next(pos, grid):
    """find next beam position(s)"""
    next_locs = []
    x, y, heading = pos
    x_next, y_next = x + heading[0], y + heading[1]
    new_loc = (x_next, y_next)
    if new_loc not in grid:
        return next_locs

    tile = grid[new_loc]
    if tile == ".":
        next_locs.append((x_next, y_next, heading))
    elif tile == "|":
        if heading in [direction["east"], direction["west"]]:
            next_locs.append((x_next, y_next, direction["north"]))
            next_locs.append((x_next, y_next, direction["south"]))
        else:
            next_locs.append((x_next, y_next, heading))
    elif tile == "-":
        if heading in [direction["north"], direction["south"]]:
            next_locs.append((x_next, y_next, direction["east"]))
            next_locs.append((x_next, y_next, direction["west"]))
        else:
            next_locs.append((x_next, y_next, heading))
    elif tile == "\\":
        if heading == direction["north"]:
            next_locs.append((x_next, y_next, direction["west"]))
        elif heading == direction["south"]:
            next_locs.append((x_next, y_next, direction["east"]))
        elif heading == direction["east"]:
            next_locs.append((x_next, y_next, direction["south"]))
        elif heading == direction["west"]:
            next_locs.append((x_next, y_next, direction["north"]))
    elif tile == "/":
        if heading == direction["north"]:
            next_locs.append((x_next, y_next, direction["east"]))
        elif heading == direction["south"]:
            next_locs.append((x_next, y_next, direction["west"]))
        elif heading == direction["east"]:
            next_locs.append((x_next, y_next, direction["north"]))
        elif heading == direction["west"]:
            next_locs.append((x_next, y_next, direction["south"]))

    return next_locs


def grid_seen(pos, grid):
    """find seen tiles based on starting position"""
    seen = []
    queue = [pos]

    while queue:
        beam = queue.pop(0)
        if beam in seen:
            continue
        seen.append(beam)
        queue.extend(beam_next(beam, grid))

    locs = {(x, y) for x, y, z in seen if (x, y) in grid}
    return len(locs)


def main():
    """loads and solves puzzle"""
    filename = "./python/2023/input/16.txt"
    lines = []
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]

    grid = {}

    for y, row in enumerate(lines):
        for x, loc in enumerate(row):
            grid[(x, y)] = loc

    edges = []
    max_x, max_y = max(k[0] for k in grid), max(k[0] for k in grid)
    # top row facing south
    # bottom row facing north
    for x in range(max_x + 1):
        edges.append((x, -1, direction["south"]))
        edges.append((x, max_y + 1, direction["north"]))
    # left col facing east
    # right col facing west
    for y in range(max_y + 1):
        edges.append((-1, y, direction["east"]))
        edges.append((max_x + 1, y, direction["west"]))

    scores = []
    for edge in edges:
        scores.append(grid_seen(edge, grid))

    print_solution(max(scores))


if __name__ == "__main__":
    main()
