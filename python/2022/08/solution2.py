
from math import prod

def printSolution(x):
    print(f"The solution is: {x}")

def scorePosition(height, trees):
    distance = 0
    for tree in trees:
        distance += 1
        if tree >= height:
            break    
    return max(distance, 1)

def main():
    file = open('../input/08.txt', 'r', encoding='utf-8')
    forest = []
    for line in file.readlines():
        trees = [int(x) for x in line.strip()]
        forest.append(trees)

    edge_min = 0
    edge_max = len(forest) - 1 

    bestScore = 0

    for y, trees in enumerate(forest):
        for x, tree in enumerate(trees):
            if edge_min in [x,y] or edge_max in [x,y]:
                continue
            else:
                left_trees = [forest[y][z] for z in range(edge_min,x)]
                right_trees = [forest[y][z] for z in range(x+1,edge_max+1)]
                up_trees = [forest[z][x] for z in range(edge_min,y)]
                down_trees = [forest[z][x] for z in range(y+1,edge_max+1)]
                # orient so side closest to treehouse has idx 0
                left_trees = left_trees[::-1]
                up_trees = up_trees[::-1]

                visibility = []
                for trees in [left_trees, right_trees, up_trees, down_trees]:
                    visibility.append(scorePosition(forest[y][x], trees))
                bestScore = max(bestScore, prod(visibility))

    printSolution(bestScore)

if __name__ == "__main__":
    main()