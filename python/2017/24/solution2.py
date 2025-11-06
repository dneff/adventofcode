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

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402


def build_longest_bridge(available_components, current_length, current_strength, connector_port):
    """Recursively build bridges and return the longest one (strongest if tied).

    Args:
        available_components: Set of remaining component tuples
        current_length: Number of components in the bridge so far
        current_strength: Running total of bridge strength so far
        connector_port: The port value that the next component must match

    Returns:
        Tuple of (length, strength) for the best bridge from this state
    """
    # Start with current bridge as the best option
    best = (current_length, current_strength)

    for component in available_components:
        if connector_port in component:
            # Determine which end connects and which is the new connector
            next_connector = component[1] if component[0] == connector_port else component[0]

            # Use set difference instead of copy + remove (much faster!)
            next_components = available_components - {component}

            # Add component and recurse
            component_strength = component[0] + component[1]
            result = build_longest_bridge(
                next_components,
                current_length + 1,
                current_strength + component_strength,
                next_connector
            )

            # Update best if this is longer, or same length but stronger
            if result[0] > best[0] or (result[0] == best[0] and result[1] > best[1]):
                best = result

    return best


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

    # Try each possible starting component
    best = (0, 0)  # (length, strength)
    for start_component in starting_components:
        next_components = remaining_components - {start_component}
        # Determine the connector port after placing the starting component
        next_connector = start_component[1] if start_component[0] == 0 else start_component[0]

        # Start with the length and strength of the starting component
        initial_strength = start_component[0] + start_component[1]
        result = build_longest_bridge(next_components, 1, initial_strength, next_connector)

        # Update best if this is longer, or same length but stronger
        if result[0] > best[0] or (result[0] == best[0] and result[1] > best[1]):
            best = result

    AoCUtils.print_solution(2, best[1])


if __name__ == "__main__":
    main()
