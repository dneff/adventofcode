"""
Advent of Code 2016 - Day 22: Grid Computing (Part 1)

Problem: Count viable pairs of storage nodes in a grid computing cluster.

A viable pair consists of two different nodes A and B where:
- Node A is not empty (used space > 0)
- The data on node A would fit on node B (A's used <= B's available)

Note: Nodes don't need to be adjacent for counting viable pairs in Part 1.
"""

from collections import defaultdict

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/22/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Node data indices
SIZE_INDEX = 0
USED_INDEX = 1
AVAIL_INDEX = 2
USAGE_PCT_INDEX = 3


def main():
    """Count the number of viable pairs of storage nodes."""
    # Parse storage nodes from input
    # Input format: /dev/grid/node-x0-y0   85T   73T    12T   85%
    storage_nodes = defaultdict(list)

    # Skip first 2 header lines and parse node data
    for line in AoCInput.read_lines(INPUT_FILE)[2:]:
        node_name, size, used, available, usage_pct = line.strip().split()

        # Extract coordinates from node name (e.g., "node-x0-y0")
        _, x_coord, y_coord = node_name.split('-')
        x_coord, y_coord = x_coord[1:], y_coord[1:]  # Remove 'x' and 'y' prefixes

        # Normalize y-coordinate to 2 digits for consistent node_id
        if len(y_coord) == 1:
            y_coord = '0' + y_coord

        node_id = x_coord + y_coord

        # Store node data: [size, used, available, usage_percentage]
        # Remove 'T' suffix from sizes and '%' from usage percentage
        storage_nodes[node_id] = [
            int(size[:-1]),
            int(used[:-1]),
            int(available[:-1]),
            int(usage_pct[:-1])
        ]

    # Count viable pairs: all combinations where A's data fits on B
    viable_pairs = 0
    for node_a in storage_nodes.keys():
        for node_b in storage_nodes.keys():
            # Nodes must be different
            if node_a == node_b:
                continue

            # Node A must not be empty
            if storage_nodes[node_a][USED_INDEX] == 0:
                continue

            # Node A's used space must fit in Node B's available space
            if storage_nodes[node_a][USED_INDEX] <= storage_nodes[node_b][AVAIL_INDEX]:
                viable_pairs += 1

    AoCUtils.print_solution(1, viable_pairs)


if __name__ == "__main__":
    main()
