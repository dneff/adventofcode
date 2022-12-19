
from collections import defaultdict, deque


def printSolution(x):
    print(f"The solution is {x}")


def findNeighbors(position):
    neighbors = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    neighbor_positions = []
    for offset in neighbors:
        neighbor_positions.append(tuple([item1 + item2 for item1, item2 in zip(offset, position)]))
    return neighbor_positions


def scoreDepth(chart, position, ignored=[]):
    neighbor_positions = []
    for n in findNeighbors(position):
        if n not in ignored:
            neighbor_positions.append(n)

    pos_depth = chart[position]
    isDeepest = [pos_depth < chart[p] for p in neighbor_positions]
    if all(isDeepest):
        return pos_depth + 1
    else:
        return 0


def scoreBasin(chart, position, found, ignored=[]):
    neighbor_positions = []
    for n in findNeighbors(position):
        if n not in ignored and n not in found:
            neighbor_positions.append(n)

    pos_depth = chart[position]
    isDeepest = [pos_depth < chart[p] for p in neighbor_positions]
    if all(isDeepest):
        return pos_depth + 1
    else:
        return 0


def findBasins(chart):
    max_row = max([x[0] for x in chart.keys()])
    max_col = max([x[1] for x in chart.keys()])
    basin_points = []
    for r in range(max_row+1):
        for c in range(max_col+1):
            position_score = scoreDepth(chart, (r, c))
            if position_score > 0:
                basin_points.append((r, c))
    return basin_points


def basinSize(chart, position, found):
    in_basin = [position]
    to_test = deque()
    to_test.extend(findNeighbors(position))

    while len(to_test) > 0:
        adjacent = to_test.popleft()
        if chart[adjacent] != 9:
            in_basin.append(adjacent)
            for new_neighbor in findNeighbors(adjacent):
                if new_neighbor not in to_test and new_neighbor not in in_basin and new_neighbor not in found:
                    to_test.append(new_neighbor)

    return(list(set(in_basin)))


def main():
    test = 'test.txt'
    puzzle = 'input.txt'
    file = open(puzzle, 'r')

    # load data
    depths = defaultdict(lambda: 9)
    row = 0
    for line in file.readlines():
        for col, x in enumerate(line.strip()):
            depths[(row, col)] = int(x)
        row += 1

    # find basins
    basin_points = findBasins(depths)

    # find basin sizes
    found = set()
    basin_sizes = []
    for bp in basin_points:
        basin_locations = basinSize(depths, bp, found)
        basin_sizes.append(basin_locations)
        found = found.union(set(basin_locations))

    # return product of three greatest basins
    basin_sizes = [len(x) for x in basin_sizes]
    basin_sizes.sort()
    printSolution(basin_sizes[-3] * basin_sizes[-2] * basin_sizes[-1])


if __name__ == "__main__":
    main()
