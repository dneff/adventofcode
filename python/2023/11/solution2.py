"""solves 2023 day 11 part 2"""

from itertools import combinations


def print_solution(x):
    """prints solution"""
    print(f"The solution is: {x}")


def expand_stars(stars, expansion):
    """expand distance based on empty columns and rows"""
    all_x = [pos[0] for pos in stars.values()]
    all_y = [pos[1] for pos in stars.values()]

    # find empty space
    empty_x, empty_y = [], []
    for x in range(max(all_x)):
        if x not in all_x:
            empty_x.append(x)

    for y in range(max(all_y)):
        if y not in all_y:
            empty_y.append(y)

    # create new expanded galaxy
    expanded = {}
    for idx, loc in enumerate(stars.values()):
        expanded_x = loc[0] + (expansion * len([x for x in empty_x if x < loc[0]]))
        expanded_y = loc[1] + (expansion * len([y for y in empty_y if y < loc[1]]))
        expanded[idx + 1] = (expanded_x, expanded_y)

    return expanded


def distance(star1, star2, stars):
    """find manhattan distance"""
    x1, y1, x2, y2 = *stars[star1], *stars[star2]
    return abs(x1 - x2) + abs(y1 - y2)


def main():
    """loads and solves puzzle"""
    expansion = 999999

    filename = "./python/2023/input/11.txt"
    lines = []
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]

    # get star locations
    stars = {}
    number = 1
    for y, line in enumerate(lines):
        for x, loc in enumerate(line):
            if loc == "#":
                stars[number] = (x, y)
                number += 1

    # expand by expansion amount
    stars = expand_stars(stars, expansion)

    # get all star path distances
    paths = combinations(stars, 2)
    all_pairs_distance = 0
    for pairs in list(paths):
        all_pairs_distance += distance(*pairs, stars)

    print_solution(all_pairs_distance)


if __name__ == "__main__":
    main()
