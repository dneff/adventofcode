import networkx as nx
import copy


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

    # generate width (x)
    x_ext = []
    for x in range(1, 5):
        extension = {}
        for k, v in weights.items():
            new_val = (v + x) % 9
            if new_val == 0:
                new_val = 9
            extension[(max_x*x + x + k[0], k[1])] = new_val
        x_ext.append(copy.copy(extension))
    for x in x_ext:
        weights.update(x)

    # generate depth (y)
    y_ext = []
    for y in range(1, 5):
        extension = {}
        for k, v in weights.items():
            new_val = (v + y) % 9
            if new_val == 0:
                new_val = 9
            extension[(k[0], max_y*y + y + k[1])] = new_val
        y_ext.append(copy.copy(extension))

    for y in y_ext:
        weights.update(y)

    # update for jumbo chart
    max_x = max([k[0] for k in weights.keys()])
    max_y = max([k[1] for k in weights.keys()])

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

    printSolution(sum(node_weights[1:]))


if __name__ == "__main__":
    main()
