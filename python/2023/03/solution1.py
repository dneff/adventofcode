"""solves AOC 2023 Day 3 - 1"""
from collections import defaultdict


def print_solution(x):
    """prints solution"""
    print(f"The solution is: {x}")


def get_adjacent(loc):
    """finds all points surrounding given loc"""
    x, y = loc
    adj = [
        (x - 1, y - 1),
        (x, y - 1),
        (x + 1, y - 1),
        (x - 1, y),
        (x + 1, y),
        (x - 1, y + 1),
        (x, y + 1),
        (x + 1, y + 1),
    ]
    return adj


def main():
    """finds solution"""
    filename = "./python/2023/input/03.txt"
    number_map = defaultdict(list)
    symbol_map = defaultdict(list)
    with open(filename, "r", encoding="utf-8") as file:
        for y, line in enumerate(file.readlines()):
            digits = []
            for x, c in enumerate(line.strip()):
                if c.isdigit():
                    digits.append((c, x, y))
                    continue
                if c != ".":
                    symbol_map[c].append((x, y))
                if len(digits) > 0:
                    number = "".join([x[0] for x in digits])
                    coordinates = [(x[1], x[2]) for x in digits]
                    adjacents = []
                    for loc in coordinates:
                        adj_locs = get_adjacent(loc)
                        adjacents.extend(adj_locs)
                    coordinates.extend(adjacents)
                    number_map[number].append(coordinates)
                    digits.clear()
            if len(digits) > 0:
                number = "".join([x[0] for x in digits])
                coordinates = [(x[1], x[2]) for x in digits]
                adjacents = []
                for loc in coordinates:
                    adj_locs = get_adjacent(loc)
                    adjacents.extend(adj_locs)
                coordinates.extend(adjacents)
                number_map[number].append(coordinates)
                digits.clear()

        symbol_locs = []
        for locs in symbol_map.values():
            symbol_locs.extend(locs)

        part_numbers = []

        for number, locs in number_map.items():
            for number_loc in locs:
                if set(symbol_locs) & set(number_loc):
                    part_numbers.append(int(number))

        print_solution(sum(part_numbers))


if __name__ == "__main__":
    main()
