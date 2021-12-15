import networkx as nx


def printSolution(x):
    print(f"The solution is {x}")


def main():
    puzzle = 'input.txt'
    test = 'test.txt'

    file = open(puzzle, 'r')

    weights = {}
    max_x = 0
    max_y = 0
    for y, line in enumerate(file.readlines()):
        for x, node in enumerate(line.strip()):
            weights[(x, y)] = int(node)
            max_x = max(max_x, x)
            max_y = max(max_y, y)

    chart = nx.generators.grid_2d_graph(
                max_x+1,
                max_y+1,
                False,
                create_using=nx.DiGraph
            )
    for source, dest in chart.edges():
        chart.edges[source, dest]["weight"] = weights[dest]

    start = (0, 0)
    end = (max_x, max_y)
    distance = nx.dijkstra_path(chart, start, end, weight="weight")
    node_weights = [weights[n] for n in distance]

    print(node_weights[1:])
    printSolution(sum(node_weights[1:]))


if __name__ == "__main__":
    main()
