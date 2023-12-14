"""solves 2023/13 part 1"""


def print_solution(x):
    """prints solution"""
    print(f"The solution is: {x}")


def find_mirror_point(grid):
    """
    find the column or row where the array is symmetrical
    find point of symmetry in rows
    """
    for i in range(1, len(grid[0])):
        symmetrical = True
        for row in grid:
            if not all([a == b for a, b in zip(row[i:], reversed(row[:i]))]):
                symmetrical = False
                break
        if symmetrical:
            return i

    rotated = list(zip(*grid))[::-1]
    rotated = ["".join(list(row)) for row in rotated]

    for i in range(1, len(rotated[0])):
        symmetrical = True
        for row in rotated:
            if not all([a == b for a, b in zip(row[i:], reversed(row[:i]))]):
                symmetrical = False
                break
        if symmetrical:
            return i * 100

    return 0


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
        score = find_mirror_point(m)
        scores.append(score)

    print_solution(sum(scores))


if __name__ == "__main__":
    main()
