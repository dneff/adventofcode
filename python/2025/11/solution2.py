"""
Advent of Code 2025 - Day 11: Reactor
https://adventofcode.com/2025/day/11

Part 2: Finding Paths with Required Waypoints

Problem:
Find all paths from 'svr' (server rack) to 'out' that visit both 'dac' and 'fft'
(in any order). The paths must pass through these two specific devices, but the
order doesn't matter.

Input Format:
Each line gives a device name followed by a list of connected output devices:
    device_name: output1 output2 output3

Example:
    bbb: ddd eee
    This means device 'bbb' has two outputs, one to 'ddd' and one to 'eee'.

Solution Strategy:
Use depth-first search (DFS) with memoization to count paths while tracking
whether required waypoints ('dac' and 'fft') have been visited. The memoization
state includes (current_node, visited_dac, visited_fft) to avoid redundant
calculations.

Optimization:
If the graph is a directed acyclic graph (DAG), we can safely use memoization
without cycle detection. Otherwise, we fall back to tracking visited nodes to
prevent infinite loops.

"""

import os
import sys
from collections import defaultdict

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "../../"))

from aoc_helpers import AoCInput, AoCUtils, Pathfinding  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, "../../../../aoc-data/2025/11/input")

# Build the device graph from input
# graph[device] = list of devices that device connects to
graph = defaultdict(list)
for line in AoCInput.read_lines(INPUT_FILE):
    device, outputs = line.split(": ")
    for output in outputs.split(" "):
        graph[device].append(output)

def is_dag(graph):
    """
    Check if graph is a directed acyclic graph (DAG) using DFS with cycle detection.

    Uses a three-color marking scheme:
    - WHITE (0): Unvisited node
    - GRAY (1): Currently being explored (in the DFS stack)
    - BLACK (2): Fully explored (all descendants visited)

    If we encounter a GRAY node during DFS, we've found a cycle.

    Args:
        graph: Dictionary mapping each node to a list of its neighbors

    Returns:
        True if the graph is acyclic, False if it contains a cycle
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = defaultdict(lambda: WHITE)

    def has_cycle(node):
        """DFS helper to detect cycles."""
        # Already fully explored - no cycle found
        if color[node] == BLACK:
            return False
        # Currently exploring - we've found a back edge (cycle)
        if color[node] == GRAY:
            return True

        # Mark as currently exploring
        color[node] = GRAY
        # Explore all neighbors
        for neighbor in graph.get(node, []):
            if has_cycle(neighbor):
                return True
        # Mark as fully explored
        color[node] = BLACK
        return False

    # Check all connected components
    for node in graph:
        if color[node] == WHITE:
            if has_cycle(node):
                return False
    return True

def count_paths_dag_optimized(graph, start, goal, visited_dac, visited_fft, memo):
    """
    Count paths from start to goal that visit both 'dac' and 'fft' (DAG version).

    This optimized version assumes the graph is a DAG, so we can use memoization
    without worrying about cycles. The memoization state includes which required
    waypoints have been visited.

    Args:
        graph: Dictionary mapping each node to a list of its neighbors
        start: Current node
        goal: Destination node
        visited_dac: Boolean indicating if 'dac' has been visited
        visited_fft: Boolean indicating if 'fft' has been visited
        memo: Dictionary for memoization {(node, dac_visited, fft_visited): count}

    Returns:
        Number of valid paths from start to goal that visit both waypoints
    """
    # Check memoization cache
    state = (start, visited_dac, visited_fft)
    if state in memo:
        return memo[state]

    # Base case: reached the goal
    if start == goal:
        # Path is valid only if both required waypoints were visited
        result = 1 if (visited_dac and visited_fft) else 0
        memo[state] = result
        return result

    # Base case: dead end (node has no outgoing edges)
    if start not in graph:
        memo[state] = 0
        return 0

    # Recursive case: explore all neighbors and sum path counts
    total_paths = 0
    for neighbor in graph[start]:
        # Update waypoint flags if we're visiting one of the required nodes
        new_dac = visited_dac or (neighbor == "dac")
        new_fft = visited_fft or (neighbor == "fft")
        paths = count_paths_dag_optimized(graph, neighbor, goal, new_dac, new_fft, memo)
        total_paths += paths

    # Cache the result before returning
    memo[state] = total_paths
    return total_paths

# Check if graph is a DAG to determine which algorithm to use
if is_dag(graph):
    # Optimized path: Use memoization without cycle checking
    memo = {}
    # Check if the starting node is one of the required waypoints
    initial_dac = ("svr" == "dac")
    initial_fft = ("svr" == "fft")
    answer = count_paths_dag_optimized(graph, "svr", "out", initial_dac, initial_fft, memo)
else:
    # Fallback path: Graph has cycles, need explicit cycle detection
    def count_with_cycles(graph, start, goal, visited_dac, visited_fft, visited_nodes):
        """
        Count paths with cycle detection (for graphs with cycles).

        Args:
            graph: Dictionary mapping each node to a list of its neighbors
            start: Current node
            goal: Destination node
            visited_dac: Boolean indicating if 'dac' has been visited
            visited_fft: Boolean indicating if 'fft' has been visited
            visited_nodes: Set of nodes visited in the current path (for cycle detection)

        Returns:
            Number of valid paths from start to goal that visit both waypoints
        """
        # Base case: reached the goal
        if start == goal:
            return 1 if (visited_dac and visited_fft) else 0

        # Base case: dead end
        if start not in graph:
            return 0

        # Recursive case: explore all neighbors
        total_paths = 0
        for neighbor in graph[start]:
            # Skip neighbors already in the current path (avoid cycles)
            if neighbor in visited_nodes:
                continue
            # Update waypoint flags
            new_dac = visited_dac or (neighbor == "dac")
            new_fft = visited_fft or (neighbor == "fft")
            # Add neighbor to visited set for this path
            new_visited = visited_nodes | {neighbor}
            paths = count_with_cycles(graph, neighbor, goal, new_dac, new_fft, new_visited)
            total_paths += paths
        return total_paths

    # Check if the starting node is one of the required waypoints
    initial_dac = ("svr" == "dac")
    initial_fft = ("svr" == "fft")
    initial_visited = frozenset(["svr"])
    answer = count_with_cycles(graph, "svr", "out", initial_dac, initial_fft, initial_visited)

# Print the solution
AoCUtils.print_solution(2, answer)