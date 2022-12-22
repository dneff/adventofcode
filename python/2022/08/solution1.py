
def printSolution(x):
    print(f"The solution is: {x}")


def main():
    file = open('../input/08.txt', 'r', encoding='utf-8')
    forest = []
    for line in file.readlines():
        trees = [int(x) for x in line.strip()]
        forest.append(trees)

    edge_min = 0
    edge_max = len(forest) - 1 

    visible = 0

    for y, trees in enumerate(forest):
        for x, tree in enumerate(trees):
            if edge_min in [x,y] or edge_max in [x,y]:
                visible += 1
            else:
                left_trees = trees[:x]
                right_trees = trees[x+1:]
                up_trees = [forest[z][x] for z in range(edge_min,y)]
                down_trees = [forest[z][x] for z in range(y+1,edge_max+1)]
                if all([x < tree for x in left_trees]) or \
                    all([x < tree for x in right_trees]) or \
                    all([x < tree for x in up_trees]) or \
                    all([x < tree for x in down_trees]):
                    visible += 1

    printSolution(visible)

if __name__ == "__main__":
    main()