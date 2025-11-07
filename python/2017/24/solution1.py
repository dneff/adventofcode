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

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402


def build_strongest_bridge(available_components, current_strength, connector_port):
    """Recursively build bridges and return the maximum strength achievable.

    Args:
        available_components: Set of remaining component tuples
        current_strength: Running total of bridge strength so far
        connector_port: The port value that the next component must match

    Returns:
        Maximum strength achievable from this state
    """
    max_strength = current_strength  # At minimum, current bridge is valid

    for component in available_components:
        if connector_port in component:
            # Determine which end connects and which is the new connector
            next_connector = component[1] if component[0] == connector_port else component[0]

            # Use set difference instead of copy + remove (much faster!)
            next_components = available_components - {component}

            # Add component strength and recurse
            component_strength = component[0] + component[1]
            strength = build_strongest_bridge(
                next_components,
                current_strength + component_strength,
                next_connector
            )
            max_strength = max(max_strength, strength)

    return max_strength


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
    max_strength = 0
    for start_component in starting_components:
        next_components = remaining_components - {start_component}
        # Determine the connector port after placing the starting component
        next_connector = start_component[1] if start_component[0] == 0 else start_component[0]

        # Start with the strength of the starting component
        initial_strength = start_component[0] + start_component[1]
        strength = build_strongest_bridge(next_components, initial_strength, next_connector)
        max_strength = max(max_strength, strength)

    AoCUtils.print_solution(1, max_strength)


if __name__ == "__main__":
    main()
