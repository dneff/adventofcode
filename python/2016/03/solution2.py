from collections import defaultdict


def printSolution(x):
    print(f"The solution is: {x}")


def isTriangle(x, y, z):
    longest = max(x, y, z)
    other_two = sum([x, y, z]) - longest
    return longest < other_two


def main():

    file = open("input.txt", "r")
    triangles = defaultdict(list)

    for idx, line in enumerate(file):
        triangle_set = idx // 3
        for triangle_idx, side in enumerate(line.split()):
            triangles[(triangle_set, triangle_idx)].append(int(side))

    triangle_count = 0
    for sides in triangles.values():
        if isTriangle(*sides):
            triangle_count += 1

    printSolution(triangle_count)


if __name__ == "__main__":
    main()
