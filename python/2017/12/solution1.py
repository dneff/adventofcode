"""
Advent of Code 2017 - Day 12: Digital Plumber (Part 1)

Find how many programs are in the group that contains program ID 0. Programs communicate
through bidirectional pipes. If program A can communicate with program B, then B can
communicate with A. Programs in a group can all communicate with each other, either
directly or through other programs in the group.

This is a graph connectivity problem - find the size of the connected component containing
node 0. The solution uses NetworkX to build a directed graph and find strongly connected
components.

Example:
    0 <-> 2
    1 <-> 1
    2 <-> 0, 3, 4
    3 <-> 2, 4
    4 <-> 2, 3, 6
    5 <-> 6
    6 <-> 4, 5

    Programs 0, 2, 3, 4, 5, and 6 are all in the same group (6 programs total).
    Program 1 is isolated in its own group.
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/12/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
import networkx as nx


def build_communication_network(lines):
    """
    Build a directed graph representing program communication pipes.

    Args:
        lines: List of strings in format "ID <-> connected_id1, connected_id2, ..."

    Returns:
        NetworkX DiGraph with bidirectional edges for all connections
    """
    network = nx.DiGraph()

    for line in lines:
        node, connections = line.strip().split(' <-> ')
        node = int(node)
        connections = [int(x) for x in connections.split(',')]

        for connected_node in connections:
            network.add_edge(node, connected_node)

    return network


def main():
    """Find size of the group containing program 0."""
    lines = AoCInput.read_lines(INPUT_FILE)
    network = build_communication_network(lines)

    # Condense the graph into strongly connected components
    # This creates a new graph where each node represents a connected component
    condensed = nx.condensation(network)

    # Node 0 in the condensed graph contains the component with the original node 0
    # The 'members' attribute contains all original nodes in this component
    group_size = len(condensed.nodes[0]['members'])

    AoCUtils.print_solution(1, group_size)


if __name__ == "__main__":
    main()
