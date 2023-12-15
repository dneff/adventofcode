"""solves for 2023/14 part 1"""


def print_solution(x):
    """prints solution"""
    print(f"The solution is: {x}")


def spin_clockwise(grid, rotations):
    """rotates grid clockwise, ninety degrees per rotation"""
    for _ in range(rotations):
        grid = list(zip(*grid[::-1]))

    grid = ["".join(list(row)) for row in grid]
    return grid


def tilt_grid(grid):
    """tilts grid to the right"""
    new_grid = []
    for row in grid:
        open_idx = []
        for idx in range(len(grid) - 1, -1, -1):
            if row[idx] == ".":
                open_idx.append(idx)
            if row[idx] == "#":
                open_idx.clear()
            if row[idx] == "O":
                if len(open_idx) > 0 and open_idx[0] > idx:
                    row = row[: open_idx[0]] + "O" + row[open_idx[0] + 1 :]
                    row = row[:idx] + "." + row[idx + 1 :]
                    open_idx.pop(0)
                    open_idx.append(idx)
        new_grid.append(row)

    return new_grid


def score_grid(grid):
    """scores grid by scanning for O. O are worth their inde value + 1"""
    score = 0
    for row in grid:
        for idx, char in enumerate(row):
            if char == "O":
                score += idx + 1
    return score


def main():
    """loads input and solves for part 1"""
    filename = "./python/2023/input/14.txt"
    lines = []
    with open(filename, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines()]

    rotated = spin_clockwise(lines, 1)
    tilted = tilt_grid(rotated)
    print_solution(score_grid(tilted))


if __name__ == "__main__":
    main()
