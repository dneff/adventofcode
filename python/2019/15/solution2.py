"""
Advent of Code 2019 - Day 15: Oxygen System - Part 2

After finding the oxygen system, determine how long it takes for oxygen to fill
the entire area. Find the longest path from the oxygen system to any other location,
which represents the time in minutes for oxygen to reach that location.
"""
import os
import sys
from collections import deque

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402
from IntCode import IntCode, InputInterrupt, OutputInterrupt  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/15/input')


def get_new_position(position, direction):
    """Calculate new position after moving in given direction."""
    direction_deltas = {
        1: (0, 1),   # North
        2: (0, -1),  # South
        4: (1, 0),   # East
        3: (-1, 0)   # West
    }
    delta = direction_deltas[direction]
    return (position[0] + delta[0], position[1] + delta[1])


def find_shortest_path_bfs(location_graph, start, end):
    """Find shortest path between two locations using BFS."""
    queue = deque([("", start)])
    visited = set()

    while queue:
        path, current = queue.popleft()
        if current == end:
            return path
        if current in visited:
            continue
        visited.add(current)

        for direction, neighbor in location_graph[current]:
            queue.append((path + direction, neighbor))

    return None


def find_longest_path(location_graph, start):
    """
    Find the longest shortest path from start to any other location.
    This represents the time for oxygen to reach the farthest point.
    """
    max_path_length = 0

    for destination in location_graph:
        if start == destination:
            continue
        path = find_shortest_path_bfs(location_graph, start, destination)
        if path:
            max_path_length = max(max_path_length, len(path))

    return max_path_length


def explore_and_map_area(program):
    """
    Explore the area using wall-following to map all locations.

    Returns:
        Tuple of (location_graph, oxygen_position)
    """
    droid = IntCode(program)
    droid.complete = False

    # Wall-following: try directions in order [north, east, south, west]
    directions = [1, 4, 2, 3]
    current_direction_index = 0

    x, y = 0, 0
    visited_positions = [(x, y)]
    oxygen_position = None

    while True:
        try:
            droid.run()
        except InputInterrupt:
            droid.input.clear()
            droid.push(directions[current_direction_index])
        except OutputInterrupt:
            status = droid.pop()

            if status == 0:
                # Hit wall, turn right
                current_direction_index = (current_direction_index + 1) % 4
            elif status == 1:
                # Moved successfully, turn left and record position
                x, y = get_new_position((x, y), directions[current_direction_index])
                visited_positions.append((x, y))
                current_direction_index = (current_direction_index - 1) % 4
            elif status == 2:
                # Found oxygen system
                x, y = get_new_position((x, y), directions[current_direction_index])
                oxygen_position = (x, y)
                visited_positions.append((x, y))

        # Stop when we've returned to origin after finding oxygen
        if (x, y) == (0, 0) and oxygen_position is not None:
            break

    # Build location graph
    location_graph = {pos: [] for pos in set(visited_positions)}
    for location in location_graph.keys():
        for direction in directions:
            neighbor = get_new_position(location, direction)
            if neighbor in location_graph.keys():
                location_graph[location].append((str(direction), neighbor))

    return location_graph, oxygen_position


def solve_part2():
    """Find how many minutes for oxygen to fill entire area."""
    program = AoCInput.read_file(INPUT_FILE).strip()
    location_graph, oxygen_position = explore_and_map_area(program)
    longest_path = find_longest_path(location_graph, oxygen_position)
    return longest_path


answer = solve_part2()
AoCUtils.print_solution(2, answer)
