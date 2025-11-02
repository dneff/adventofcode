import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/12/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
import networkx as nx


def main():
    network = nx.DiGraph()
    lines = AoCInput.read_lines(INPUT_FILE)
    for line in lines:
        node, connections = line.strip().split(' <-> ')
        node = int(node)
        connections = [int(x) for x in connections.split(',')]
        for c in connections:
            network.add_edge(node,c)

    view = nx.condensation(network)
    AoCUtils.print_solution(1, len(view.nodes[0]['members']))


if __name__ == "__main__":
    main()
