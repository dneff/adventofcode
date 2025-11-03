"""
Advent of Code 2017 - Day 12: Digital Plumber (Part 2)

Count the total number of distinct groups in the communication network. Each group is a
set of programs that can all communicate with each other (directly or indirectly), but
cannot communicate with programs in other groups.

This is equivalent to counting the number of connected components (or strongly connected
components in a directed graph) in the network.
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
    """Count the total number of distinct program groups."""
    lines = AoCInput.read_lines(INPUT_FILE)
    network = build_communication_network(lines)

    # Condense the graph into strongly connected components
    condensed = nx.condensation(network)

    # The mapping values represent which component each original node belongs to
    # The number of unique component IDs is the number of groups
    num_groups = len(set(condensed.graph['mapping'].values()))

    AoCUtils.print_solution(2, num_groups)


if __name__ == "__main__":
    main()
