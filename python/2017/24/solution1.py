"""
Advent of Code 2017 - Day 24: Electromagnetic Moat (Part 1)

Build the strongest bridge from magnetic components to cross a pit.
Components have two ports that can connect when types match.
The bridge must start with a 0-port and each component can only be used once.

The strength of a bridge is the sum of all port values in the components used.

Example: bridge 0/1--10/1--9/10 has strength 0+1+10+1+9+10 = 31

The goal is to find the maximum possible strength of any valid bridge.
"""
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/24/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
from copy import deepcopy


def calculate_bridge_strength(bridge):
    """Calculate the total strength of a bridge.

    Args:
        bridge: List of component tuples (port1, port2)

    Returns:
        Sum of all port values in the bridge
    """
    sum_tuple = [sum(x) for x in zip(*bridge)]
    return sum(sum_tuple)


def build_strongest_bridge(available_components, current_bridge, connector_port):
    """Recursively build bridges and return the maximum strength achievable.

    Args:
        available_components: Set of remaining component tuples
        current_bridge: List of components already in the bridge
        connector_port: The port value that the next component must match

    Returns:
        Maximum strength achievable from this state
    """
    if len(available_components) == 0:
        return calculate_bridge_strength(current_bridge)

    possible_strengths = []
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
            possible_strengths.append(
                build_strongest_bridge(next_components, next_bridge, next_connector)
            )

    # If no more components can connect, return current bridge strength
    if len(possible_strengths) == 0:
        return calculate_bridge_strength(current_bridge)

    return max(possible_strengths)


def main():
    """Find the strength of the strongest possible bridge."""
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

    # Try each possible starting component
    max_strengths = []
    for start_component in starting_components:
        next_components = remaining_components.difference({start_component})
        # Determine the connector port after placing the starting component
        if start_component.index(0) == 0:
            next_connector = start_component[1]
        else:
            next_connector = start_component[0]

        initial_bridge = [deepcopy(start_component)]
        max_strengths.append(
            build_strongest_bridge(next_components, initial_bridge, next_connector)
        )

    AoCUtils.print_solution(1, max(max_strengths))


if __name__ == "__main__":
    main()
