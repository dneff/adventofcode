"""
Advent of Code 2019 - Day 15: Oxygen System - Part 1

Control a repair droid via Intcode to explore a ship and find the oxygen system.
The droid responds to movement commands (1=north, 2=south, 3=west, 4=east) and
reports status (0=wall, 1=moved, 2=found oxygen). Use wall-following algorithm
to map the area and find the shortest path to the oxygen system using BFS.
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
    """
    Find shortest path between two locations using BFS.

    Args:
        location_graph: Dict mapping position -> list of (direction, neighbor) tuples
        start: Starting position
        end: Target position

    Returns:
        Path as string of direction commands
    """
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


def solve_part1():
    """Find shortest path from start to oxygen system."""
    program = AoCInput.read_file(INPUT_FILE).strip()
    location_graph, oxygen_position = explore_and_map_area(program)
    shortest_path = find_shortest_path_bfs(location_graph, oxygen_position, (0, 0))
    return len(shortest_path)


answer = solve_part1()
AoCUtils.print_solution(1, answer)
