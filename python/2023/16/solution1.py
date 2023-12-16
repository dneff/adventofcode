"""solves day 16 problem 1"""


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


def display_grid(grid, seen):
    """display seen locs on grid"""
    overlay = grid.copy()
    for loc in seen:
        x, y, heading = loc
        if (x,y) not in grid:
            continue
        if grid[(x, y)] != ".":
            continue
        if heading == direction["north"]:
            overlay[(x, y)] = "^"
        elif heading == direction["south"]:
            overlay[(x, y)] = "v"
        elif heading == direction["east"]:
            overlay[(x, y)] = ">"
        elif heading == direction["west"]:
            overlay[(x, y)] = "<"

    max_x, max_y = max(k[0] for k in overlay), max(k[0] for k in overlay)
    for y in range(max_y + 1):
        row = ""
        for x in range(max_x + 1):
            if (x, y) not in overlay:
                row += "."
            else:
                row += overlay[(x, y)]
        print(row)


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

    seen = []
    queue = [(-1, 0, direction["east"])]

    while queue:
        beam = queue.pop(0)
        if beam in seen:
            continue
        seen.append(beam)
        queue.extend(beam_next(beam, grid))

    locs = {(x, y) for x, y, z in seen if (x,y) in grid}
    #display_grid(grid, seen)
    print_solution(len(locs))


if __name__ == "__main__":
    main()
