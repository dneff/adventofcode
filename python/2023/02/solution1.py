from collections import defaultdict


def print_solution(x):
    """print solution"""
    print(f"The solution is {x}")


def cubes_seen(grabs):
    """returns dict of seen cubes"""
    seen = defaultdict(int)
    for grab in grabs:
        cubes = grab.split(",")
        for group in cubes:
            count, color = group.split()
            seen[color] = max(seen[color], int(count))
    return seen


def is_valid(bag, seen):
    """verify seen could be found in bag"""
    for color, count in seen.items():
        if color not in bag:
            return False
        if bag[color] < count:
            return False
    return True


def main():
    """find solution"""
    filename = "./python/2023/input/02.txt"
    bag = {"red": 12, "green": 13, "blue": 14}
    score = 0
    with open(filename, "r", encoding="utf-8") as file:
        for line in file.readlines():
            game, grabs = line.strip().split(": ")
            game = int(game.split()[1])
            grabs = grabs.split("; ")
            seen = cubes_seen(grabs)
            if is_valid(bag, seen):
                score += game
    print_solution(score)


if __name__ == "__main__":
    main()
