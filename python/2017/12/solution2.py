import networkx as nx

def print_solution(x):
    """Format the input to print as solution"""
    print(f"The solution is: {x}")


def main():
    network = nx.DiGraph()
    file = open('input.txt', 'r', encoding='utf-8')
    for line in file.readlines():
        node, connections = line.strip().split(' <-> ')
        node = int(node)
        connections = [int(x) for x in connections.split(',')]
        for c in connections:
            network.add_edge(node,c)

    view = nx.condensation(network)
    print_solution(len(set(view.graph['mapping'].values())))


if __name__ == "__main__":
    main()
