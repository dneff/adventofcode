"""
Advent of Code 2019 - Day 18: Many-Worlds Interpretation - Part 1

Navigate a maze to collect all keys. Keys (lowercase letters) unlock doors
(uppercase letters). Find the shortest path that collects all keys.

This uses dynamic programming with memoization to explore all possible paths
and find the minimum steps needed.
"""
import os
import sys
from collections import defaultdict, deque
from functools import lru_cache
from math import inf
import heapq

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/18/input')

# Global graph for reachability
graph = {}


@lru_cache(2**20)
def find_minimum_steps(current_position, keys_remaining, keys_collected=frozenset()):
    """
    Find minimum steps to collect all remaining keys.

    Args:
        current_position: Current position character
        keys_remaining: Number of keys left to collect
        keys_collected: Frozenset of keys already collected

    Returns:
        Minimum steps needed
    """
    global graph

    if keys_remaining == 0:
        return 0

    best_steps = inf

    for next_position in current_position:
        for key_name, distance in find_reachable_keys(next_position, keys_collected):
            new_keys = keys_collected | {key_name}
            new_position = current_position.replace(next_position, key_name)

            steps = distance + find_minimum_steps(new_position, keys_remaining - 1, new_keys)

            if steps < best_steps:
                best_steps = steps

    return best_steps


@lru_cache(2**20)
def find_reachable_keys(start, collected_keys):
    """
    Find all keys reachable from start position with current keys.

    Args:
        start: Starting node
        collected_keys: Keys already collected

    Returns:
        List of (key_name, distance) tuples for reachable keys
    """
    global graph
    distances = defaultdict(lambda: inf)
    priority_queue = []
    reachable = []

    # Add immediate neighbors
    for neighbor, weight in graph[start]:
        heapq.heappush(priority_queue, (weight, neighbor))

    while priority_queue:
        dist, node = heapq.heappop(priority_queue)

        # Found a new key
        if node.islower() and node not in collected_keys:
            reachable.append((node, dist))
            continue

        # Check if we can pass through (have key for door)
        if node.lower() not in collected_keys:
            continue

        # Explore neighbors
        for neighbor, weight in graph[node]:
            new_dist = dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(priority_queue, (new_dist, neighbor))

    return reachable


def find_adjacent_nodes(maze_graph, key_positions, start):
    """
    Find adjacent key/door nodes from a starting position.

    Returns list of (key_name, distance) tuples.
    """
    queue = deque()
    visited = {start}
    found = []

    for neighbor in maze_graph[start]:
        queue.append((1, neighbor))

    while queue:
        dist, node = queue.popleft()
        if node not in visited:
            visited.add(node)

            if node in key_positions.values():
                key_name = [k for k, v in key_positions.items() if v == node][0]
                if key_name not in ['@'] and key_name not in [f[0] for f in found]:
                    found.append((key_name, dist))
                    continue

            for neighbor in maze_graph[node]:
                if neighbor not in visited:
                    queue.append((dist + 1, neighbor))

    return found


def solve_part1():
    """Find minimum steps to collect all keys in the maze."""
    global graph
    graph = defaultdict(list)
    key_positions = {}

    lines = AoCInput.read_lines(INPUT_FILE)
    maze = [line.strip() for line in lines if not line.startswith(';')]

    # Parse maze into graph
    for y, row in enumerate(maze):
        for x, char in enumerate(row):
            if char != "#":
                graph[(x, y)] = []
                if char != '.':
                    key_positions[char] = (x, y)

    # Build adjacency list
    for position in graph.keys():
        for dx, dy in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
            neighbor = (position[0] + dx, position[1] + dy)
            if neighbor in graph.keys() and neighbor not in graph[position]:
                graph[position].append(neighbor)

    # Build compressed graph with only key nodes
    compressed_graph = {}
    for key_name, position in key_positions.items():
        compressed_graph[key_name] = find_adjacent_nodes(graph, key_positions, position)

    graph = compressed_graph
    total_keys = sum(node.islower() for node in compressed_graph)
    minimum_steps = find_minimum_steps('@', total_keys)

    return minimum_steps


answer = solve_part1()
AoCUtils.print_solution(1, answer)
