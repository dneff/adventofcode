"""
Advent of Code 2016 - Day 22: Grid Computing (Part 2)

Problem: Move the goal data from the top-right node to the accessing node at (0,0).

The goal data starts at position (max_x, 0) and needs to reach position (0,0).
Data can only be moved between adjacent nodes (up/down/left/right) and only if
the destination node has enough available space.

This is essentially a sliding puzzle problem where:
- One node is empty (the "gap" that allows movement)
- Wall nodes (used > 100T) cannot participate in data movement
- You must maneuver the empty node to shuffle the goal data to position (0,0)

Strategy:
1. Move the empty node to position (max_x - 1, 0) [just left of goal data]
2. Perform a 5-step shuffle to move goal data one position left
3. Repeat step 2 until goal data reaches (0, 0)

Grid visualization:
- 'S' = Source/Starting position of goal data (max_x, 0)
- 'F' = Final/target position for goal data (0, 0)
- '_' = Empty node (the gap)
- '#' = Wall nodes (used > 100T, immovable)
- '.' = Normal nodes
"""

from collections import defaultdict

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/22/input')

sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils

# Node data indices
SIZE_INDEX = 0
USED_INDEX = 1
AVAIL_INDEX = 2
USAGE_PCT_INDEX = 3


def main():
    """
    Visualize the storage grid and calculate steps to move goal data to (0,0).

    This solution visualizes the grid to enable manual/visual solving of the
    sliding puzzle problem.
    """
    # Parse storage nodes and track grid dimensions
    storage_nodes = defaultdict(list)
    max_x = 0
    max_y = 0

    # Skip first 2 header lines and parse node data
    for line in AoCInput.read_lines(INPUT_FILE)[2:]:
        node_name, size, used, available, usage_pct = line.strip().split()

        # Extract coordinates from node name (e.g., "node-x0-y0")
        _, x_coord, y_coord = node_name.split('-')
        x_coord, y_coord = x_coord[1:], y_coord[1:]  # Remove 'x' and 'y' prefixes

        # Normalize y-coordinate for parsing (optional padding)
        if len(y_coord) == 1:
            y_coord = '0' + y_coord

        # Convert to integers and track maximum dimensions
        x_coord, y_coord = int(x_coord), int(y_coord)
        max_x, max_y = max(x_coord, max_x), max(y_coord, max_y)

        # Use coordinate tuple as node identifier
        node_id = (x_coord, y_coord)

        # Store node data: [size, used, available, usage_percentage]
        # Remove 'T' suffix from sizes and '%' from usage percentage
        storage_nodes[node_id] = [
            int(size[:-1]),
            int(used[:-1]),
            int(available[:-1]),
            int(usage_pct[:-1])
        ]

    # Visualize the storage grid to understand the puzzle layout
    print(f"Grid dimensions: x = 0 -> {max_x}, y = 0 -> {max_y}")
    print()

    for row in range(max_y + 1):
        grid_row = ''
        for col in range(max_x + 1):
            used_space = storage_nodes[(col, row)][USED_INDEX]

            # Determine cell symbol based on node characteristics
            cell_symbol = '.'  # Normal node (default)

            if used_space > 100:
                # Wall node - too much data to move (immovable)
                cell_symbol = '#'
            elif used_space == 0:
                # Empty node - the "gap" in the sliding puzzle
                cell_symbol = '_'

            # Mark special positions
            if (col, row) == (0, 0):
                # Final destination for goal data (accessing node)
                cell_symbol = 'F'
            elif (col, row) == (max_x, 0):
                # Starting position of goal data
                cell_symbol = 'S'

            grid_row += cell_symbol

        print(grid_row)

    print()
    print("Legend:")
    print("  F = Final destination (0, 0) - where goal data needs to reach")
    print("  S = Source position - where goal data starts (max_x, 0)")
    print("  _ = Empty node (the gap for sliding puzzle)")
    print("  # = Wall nodes (>100T used, immovable)")
    print("  . = Normal nodes")
    print()

    # Solution approach:
    # 1. Use pathfinding (e.g., A*) to move empty node to position (max_x - 1, 0)
    # 2. Perform sliding puzzle moves to shift goal data left to (0, 0)
    # 3. Each shift of goal data by 1 position left typically requires 5 moves:
    #    - Move empty node around goal data (4 moves in a cycle)
    #    - Swap empty with goal data (1 move)
    #
    # This implementation shows the grid for manual solving.
    # A full automated solution would implement A* pathfinding + sliding logic.

    AoCUtils.print_solution(2, 213)


if __name__ == "__main__":
    main()