"""
Advent of Code 2017 - Day 24: Electromagnetic Moat (Part 2)

Part 2 asks for the strength of the longest bridge. If multiple bridges tie
for longest, choose the one with the greatest strength.

The solution builds all possible bridges and tracks both length and strength,
then selects the bridge(s) with maximum length and returns the strongest
among those.
"""
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/24/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
from copy import deepcopy
from collections import defaultdict


def calculate_bridge_strength(bridge):
    """Calculate the total strength of a bridge.

    Args:
        bridge: List of component tuples (port1, port2)

    Returns:
        Sum of all port values in the bridge
    """
    sum_tuple = [sum(x) for x in zip(*bridge)]
    return sum(sum_tuple)


def build_longest_bridge(available_components, current_bridge, connector_port):
    """Recursively build bridges and return the longest one (strongest if tied).

    Args:
        available_components: Set of remaining component tuples
        current_bridge: List of components already in the bridge
        connector_port: The port value that the next component must match

    Returns:
        The bridge list (longest possible from this state)
    """
    if len(available_components) == 0:
        return current_bridge

    # Group possible bridges by length
    bridges_by_length = defaultdict(list)
    for component in available_components:
        if connector_port in component:
            # Determine which end connects and which is the new connector
            if component.index(connector_port) == 0:
                next_connector = component[1]
            else:
                next_connector = component[0]

            # Build new state with this component added
            next_components = deepcopy(available_components)
            next_components.remove(component)
            next_bridge = deepcopy(current_bridge)
            next_bridge.append(deepcopy(component))

            # Recursively explore this path
            resulting_bridge = build_longest_bridge(next_components, next_bridge, next_connector)
            bridges_by_length[len(resulting_bridge)].append(resulting_bridge)

    # If no more components can connect, return current bridge
    if len(bridges_by_length.keys()) == 0:
        return current_bridge

    # Find the longest bridge(s)
    longest_length = max(bridges_by_length.keys())
    longest_bridges = bridges_by_length[longest_length]

    # Among longest bridges, find the strongest
    strengths = [calculate_bridge_strength(b) for b in longest_bridges]
    strongest_index = strengths.index(max(strengths))
    return longest_bridges[strongest_index]


def main():
    """Find the strength of the longest possible bridge (strongest if tied)."""
    lines = AoCInput.read_lines(INPUT_FILE)

    # Parse all available components
    all_components = set()
    for line in lines:
        port_a, port_b = [int(x) for x in line.split('/')]
        all_components.add((port_a, port_b))

    # Find components that can start the bridge (have a 0 port)
    starting_components = set()
    for component in all_components:
        if component[0] == 0:
            starting_components.add(component)

    # Remove starting components from the main pool
    remaining_components = all_components.difference(starting_components)

    # Try each possible starting component and group results by length
    bridges_by_length = defaultdict(list)
    for start_component in starting_components:
        next_components = remaining_components.difference({start_component})
        # Determine the connector port after placing the starting component
        if start_component.index(0) == 0:
            next_connector = start_component[1]
        else:
            next_connector = start_component[0]

        initial_bridge = [deepcopy(start_component)]
        resulting_bridge = build_longest_bridge(next_components, initial_bridge, next_connector)
        bridges_by_length[len(resulting_bridge)].append(resulting_bridge)

    # Find the longest bridge(s)
    longest_length = max(bridges_by_length.keys())
    longest_bridges = bridges_by_length[longest_length]

    # Among longest bridges, find the strongest
    strengths = [calculate_bridge_strength(b) for b in longest_bridges]
    strongest_index = strengths.index(max(strengths))
    final_bridge = longest_bridges[strongest_index]

    AoCUtils.print_solution(2, calculate_bridge_strength(final_bridge))


if __name__ == "__main__":
    main()
