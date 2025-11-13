"""
Advent of Code 2019 - Day 18: Many-Worlds Interpretation - Part 2

The maze now has 4 robots starting from 4 different positions (the entrance
is divided into 4 quadrants). Each robot can move independently. Find the
minimum total steps for all robots to collect all keys.
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
def find_minimum_steps(current_positions, keys_remaining, keys_collected=frozenset()):
    """
    Find minimum steps for all robots to collect remaining keys.

    Args:
        current_positions: String with 4 robot positions
        keys_remaining: Number of keys left to collect
        keys_collected: Frozenset of keys already collected

    Returns:
        Minimum steps needed
    """
    global graph

    if keys_remaining == 0:
        return 0

    best_steps = inf

    for robot_position in current_positions:
        for key_name, distance in find_reachable_keys(robot_position, keys_collected):
            new_keys = keys_collected | {key_name}
            new_positions = current_positions.replace(robot_position, key_name)

            steps = distance + find_minimum_steps(new_positions, keys_remaining - 1, new_keys)

            if steps < best_steps:
                best_steps = steps

    return best_steps


@lru_cache(2**20)
def find_reachable_keys(start, collected_keys):
    """Find all keys reachable from start position with current keys."""
    global graph
    distances = defaultdict(lambda: inf)
    priority_queue = []
    reachable = []

    for neighbor, weight in graph[start]:
        heapq.heappush(priority_queue, (weight, neighbor))

    while priority_queue:
        dist, node = heapq.heappop(priority_queue)

        if node.islower() and node not in collected_keys:
            reachable.append((node, dist))
            continue

        if node.lower() not in collected_keys:
            continue

        for neighbor, weight in graph[node]:
            new_dist = dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(priority_queue, (new_dist, neighbor))

    return reachable


def find_adjacent_nodes(maze_graph, key_positions, start):
    """Find adjacent key/door nodes from a starting position."""
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
                if key_name not in ['@', '1', '2', '3', '4'] and key_name not in [f[0] for f in found]:
                    found.append((key_name, dist))
                    continue

            for neighbor in maze_graph[node]:
                if neighbor not in visited:
                    queue.append((dist + 1, neighbor))

    return found


def solve_part2():
    """Find minimum steps for 4 robots to collect all keys."""
    global graph
    find_minimum_steps.cache_clear()
    find_reachable_keys.cache_clear()

    graph = defaultdict(list)
    key_positions = {}

    lines = AoCInput.read_lines(INPUT_FILE)
    maze = [line.strip() for line in lines if not line.startswith(';')]

    # Modify part 2 maze for 4 robots
    mid_x = len(maze[0]) // 2
    mid_y = len(maze) // 2
    maze[mid_y - 1] = maze[mid_y - 1][:mid_x - 1] + "@#@" + maze[mid_y - 1][mid_x + 2:]
    maze[mid_y + 0] = maze[mid_y + 0][:mid_x - 1] + "###" + maze[mid_y + 0][mid_x + 2:]
    maze[mid_y + 1] = maze[mid_y + 1][:mid_x - 1] + "@#@" + maze[mid_y + 1][mid_x + 2:]

    # Parse maze (4 @ symbols become robots 1,2,3,4)
    robot_number = 1
    for y, row in enumerate(maze):
        for x, char in enumerate(row):
            if char != "#":
                graph[(x, y)] = []
                if char != '.':
                    if char == '@':
                        key_positions[str(robot_number)] = (x, y)
                        robot_number += 1
                    else:
                        key_positions[char] = (x, y)

    # Build adjacency list
    for position in graph.keys():
        for dx, dy in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
            neighbor = (position[0] + dx, position[1] + dy)
            if neighbor in graph.keys() and neighbor not in graph[position]:
                graph[position].append(neighbor)

    # Build compressed graph
    compressed_graph = {}
    for key_name, position in key_positions.items():
        compressed_graph[key_name] = find_adjacent_nodes(graph, key_positions, position)

    graph = compressed_graph
    total_keys = sum(node.islower() for node in compressed_graph)
    minimum_steps = find_minimum_steps('1234', total_keys)

    return minimum_steps


answer = solve_part2()
AoCUtils.print_solution(2, answer)
