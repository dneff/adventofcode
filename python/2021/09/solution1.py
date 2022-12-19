
from collections import defaultdict


def printSolution(x):
    print(f"The solution is {x}")


def scoreDepth(chart, position):
    neighbors = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    neighbor_positions = []
    for offset in neighbors:
        neighbor_positions.append(tuple([item1 + item2 for item1, item2 in zip(offset, position)]))

    pos_depth = chart[position]
    isDeepest = [pos_depth < chart[p] for p in neighbor_positions]
    if all(isDeepest):
        return pos_depth + 1
    else:
        return 0


def main():
    test = 'test.txt'
    puzzle = 'input.txt'
    file = open(puzzle, 'r')

    depths = defaultdict(lambda: 9)

    row = 0
    for line in file.readlines():
        for col, x in enumerate(line.strip()):
            depths[(row, col)] = int(x)
        row += 1

    max_row = max([x[0] for x in depths.keys()])
    max_col = max([x[1] for x in depths.keys()])

    depth_scores = []
    for c in range(max_col+1):
        for r in range(max_row+1):
            position_score = scoreDepth(depths, (r, c))
            if position_score > 0:
                depth_scores.append(position_score)

    printSolution(sum(depth_scores))

if __name__ == "__main__":
    main()
