from collections import defaultdict
import copy


def printSolution(x):
    print(f"The solution is {x}")


class Cave:
    def __init__(self, chart):
        self.chart = copy.deepcopy(chart)
        self.position = 'start'
        self.seen = ['start', 'start']


def findPaths(cave):
    paths = []

    if cave.position == 'end':
        paths.append('-'.join(cave.seen))
        return paths
    for p in cave.chart[cave.position]:
        if (p.islower() and cave.seen.count(p) < 1) or (p.isupper()) or p == 'end':
            new_cave = copy.deepcopy(cave)
            new_cave.position = p
            new_cave.seen.append(p)
            paths.extend(findPaths(new_cave))

    return list(set(paths))


def main():
    test = 'test.txt'
    puzzle = 'input.txt'

    chart = defaultdict(list)

    file = open(puzzle, 'r')
    for line in file.readlines():
        node1, node2 = line.strip().split('-')
        chart[node1].append(node2)
        chart[node2].append(node1)

    cave = Cave(chart)
    all_paths = findPaths(cave)

    printSolution(len(all_paths))


if __name__ == "__main__":
    main()
