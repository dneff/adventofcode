"""
Advent of Code 2025 - Day 11: Reactor
https://adventofcode.com/2025/day/11

Part 1: Finding All Paths Through the Reactor Network

Problem:
Given a directed graph of devices where each device has outputs connecting to other
devices, find all possible paths from the starting device 'you' to the output device 'out'.

Input Format:
Each line gives a device name followed by a list of connected output devices:
    device_name: output1 output2 output3

Example:
    bbb: ddd eee
    This means device 'bbb' has two outputs, one to 'ddd' and one to 'eee'.

Solution:
Use depth-first search (DFS) to enumerate all paths, avoiding cycles by tracking
visited nodes within each path.

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

def get_all_paths(graph, start, goal, path=None):
    """
    Find all paths from start to goal in a directed graph using DFS.

    Args:
        graph: Dictionary mapping each node to a list of its neighbors
        start: Starting node
        goal: Destination node
        path: Current path being explored (internal use, defaults to None)

    Returns:
        List of all paths from start to goal, where each path is a list of nodes
    """
    # Initialize path on first call (avoid mutable default argument)
    if path is None:
        path = []

    # Add current node to the path
    path = path + [start]

    # Base case: reached the goal
    if start == goal:
        return [path]

    # Base case: dead end (node has no outgoing edges)
    if start not in graph:
        return []

    # Recursive case: explore all neighbors
    paths = []
    for neighbor in graph[start]:
        # Avoid cycles by not revisiting nodes in the current path
        if neighbor not in path:
            new_paths = get_all_paths(graph, neighbor, goal, path)
            for new_path in new_paths:
                paths.append(new_path)

    return paths


# Find all paths from 'you' to 'out' and count them
all_paths = get_all_paths(graph, "you", "out")
answer = len(all_paths)

# Print the solution
AoCUtils.print_solution(1, answer)

