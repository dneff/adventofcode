"""solves 2023 day 11 part 1"""

from itertools import combinations


def print_solution(x):
    """prints solution"""
    print(f"The solution is: {x}")


def expand(galaxy):
    """add empty row and column in empty locations"""
    expanded = []
    # expand rows
    for row in galaxy:
        expanded.append(row)
        if len(set(row[:])) == 1:
            expanded.append(row)
    # expand columns
    new_cols = []
    for idx in range(len(galaxy[0])):
        column = [row[idx] for row in galaxy]
        if len(set(column[:])) == 1:
            new_cols.append(idx)
    new_cols = sorted(new_cols, reverse=True)
    result = []
    for row in expanded:
        for col in new_cols:
            row = row[:col] + "." + row[col:]
        result.append(row)
    return result


def distance(star1, star2, stars):
    """find manhattan distance"""
    x1, y1, x2, y2 = *stars[star1], *stars[star2]
    return abs(x1 - x2) + abs(y1 - y2)


def main():
    """loads and solves puzzle"""
    filename = "./python/2023/input/11.txt"
    lines = []
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]

    galaxy = expand(lines)

    # get star locations
    stars = {}
    number = 1
    for y, line in enumerate(galaxy):
        for x, loc in enumerate(line):
            if loc == "#":
                stars[number] = (x, y)
                number += 1

    # get all star path distances
    paths = combinations(stars, 2)
    all_pairs_distance = 0
    for pairs in list(paths):
        all_pairs_distance += distance(*pairs, stars)

    print_solution(all_pairs_distance)


if __name__ == "__main__":
    main()
