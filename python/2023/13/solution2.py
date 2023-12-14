"""solves 2023/13 part 1"""


def print_solution(x):
    """prints solution"""
    print(f"The solution is: {x}")


def find_smudges(grid):
    """
    find the column or row where the array is almost symmetrical
    find point of symmetry in rows that's off by 1
    """
    solution = 0
    for i in range(1, len(grid[0])):
        diff_count = 0
        for row in grid:
            diff_count += len([1 for a, b in zip(row[i:], reversed(row[:i])) if a != b])
        if diff_count == 1:
            solution = i

    rotated = list(zip(*grid))[::-1]
    rotated = ["".join(list(row)) for row in rotated]

    for i in range(1, len(rotated[0])):
        diff_count = 0
        for row in rotated:
            diff_count += len([1 for a, b in zip(row[i:], reversed(row[:i])) if a != b])
        if diff_count == 1:
            solution = i * 100

    return solution


def main():
    """main"""
    filename = "./python/2023/input/13.txt"
    lines = []
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()

    maps = []
    current = []
    for line in lines:
        if len(line.strip()) == 0:
            maps.append(current.copy())
            current.clear()
        else:
            current.append(line.strip())
    maps.append(current.copy())

    scores = []
    for m in maps:
        score = find_smudges(m)
        scores.append(score)

    print_solution(sum(scores))


if __name__ == "__main__":
    main()
