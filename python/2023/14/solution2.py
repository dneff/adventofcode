"""solves for 2023/14 part 2"""


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
    """scores grid by scanning for O. O are worth their index value + 1"""
    score = 0
    for row in grid:
        for idx, char in enumerate(row):
            if char == "O":
                score += idx + 1
    return score


def spin_cycle(grid):
    """rotates and tilt the grid 4 times"""
    for _ in range(4):
        rotated = spin_clockwise(grid, 1)
        tilted = tilt_grid(rotated)
        grid = tilted
    return grid


def main():
    """loads input and solves for part 2"""
    filename = "./python/2023/input/14.txt"
    lines = []
    with open(filename, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines()]

    total_cycles = 1000000000
    # find repeating pattern
    iterations = 5000
    scores = []
    for _ in range(iterations):
        lines = spin_cycle(lines)
        # get the north score
        scores.append(score_grid(spin_clockwise(lines, 1)))

    counts = {}
    for score in scores:
        if score not in counts:
            counts[score] = 0
        counts[score] += 1

    high_repeats = []
    for score, count in counts.items():
        if count > 100:
            high_repeats.append(score)

    # find sequence of high repeats in scores
    sequence = []
    sequence_start = None
    for idx, score in enumerate(scores):
        if set(high_repeats).issubset(scores[idx : idx + len(high_repeats)]):
            sequence_start = idx
            sequence = scores[idx : idx + len(high_repeats)]
            break

    # idx off by one from cycles
    sequence_start += 1

    # jump forward by sequence length
    final_score = sequence[(total_cycles - sequence_start) % len(sequence)]
    # 106682 too low
    print_solution(final_score)


if __name__ == "__main__":
    main()
