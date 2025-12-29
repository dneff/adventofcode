"""
Advent of Code 2022 - Day 16: Proboscidea Volcanium
https://adventofcode.com/2022/day/16

Navigate a network of valves and tunnels to maximize pressure release.
Find the best path to open valves within 30 minutes to maximize total flow.
"""

import os
import sys
from collections import deque
from itertools import permutations

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2022/16/input')


def generate_rooms(lines):
    """
    Parse input and generate graph of rooms with valves and tunnels.

    Args:
        lines: List of input lines describing valves

    Returns:
        dict: Graph where keys are room names, values contain flow rate and connected tunnels
    """
    graph = {}

    for line in lines:
        room = line.split()[1]
        flow = line.split("=")[1].split(";")[0]
        flow = int(flow)
        tunnels = line.split("valve")[1].strip().strip("s ").split(", ")
        graph[room] = {"flow": flow, "tunnels": tunnels}

    return graph


def best_path(start, valve_cache, distance_cache, duration):
    """
    Find the best path through valves to maximize pressure release.

    Uses BFS to explore all possible paths of opening valves, tracking:
    - Current path (sequence of rooms visited)
    - Remaining time
    - Current flow rate (sum of opened valves)
    - Total pressure released so far

    Args:
        start: Starting room name
        valve_cache: Dictionary of valve rooms to their flow rates
        distance_cache: Pre-computed distances between all valve pairs
        duration: Total time available

    Returns:
        int: Maximum total pressure that can be released
    """
    best_score = 0
    queue = deque()

    # Queue entry: (path, remaining_time, flow_rate, total_score)
    queue.append(((start,), duration, 0, 0))

    while queue:
        path, time, flow, score = queue.popleft()

        # Find unvisited rooms with valves
        next_room = [x for x in valve_cache.keys() if x not in path]

        # If no more rooms to visit, accumulate remaining time
        if len(next_room) == 0:
            score += flow * time
            best_score = max(best_score, score)
            continue

        # Try visiting each remaining valve
        for room in next_room:
            travel_time = distance_cache[(path[-1], room)]

            # If not enough time to reach and open this valve
            if time < travel_time:
                # Just accumulate remaining time
                final_score = score + flow * time
                best_score = max(best_score, final_score)
            else:
                # Travel to room, open valve, update state
                next_path = path + (room,)
                next_time = time - travel_time
                next_flow = flow + valve_cache[room]
                next_score = score + (travel_time * flow)
                queue.append((next_path, next_time, next_flow, next_score))

    return best_score


def breadth_search(start, end, rooms):
    """
    Find shortest path length between two rooms using BFS.

    Args:
        start: Starting room name
        end: Destination room name
        rooms: Graph of rooms and tunnels

    Returns:
        int: Length of shortest path (number of moves)
    """
    queue, seen = deque(), set()
    queue.append([start])

    while queue:
        path = queue.popleft()
        room = path[-1]

        if room not in seen:
            seen.add(room)
            if room == end:
                return len(path) - 1

            for location in rooms[room]["tunnels"]:
                new_path = path[:]
                new_path.append(location)
                queue.append(new_path)


def solve_part1():
    """
    Find the maximum pressure that can be released in 30 minutes.

    Returns:
        int: Maximum total pressure released
    """
    lines = AoCInput.read_lines(INPUT_FILE)
    rooms = generate_rooms(lines)

    # Find all rooms with non-zero flow rates
    valve_rooms = [k for k, v in rooms.items() if v["flow"] > 0]

    start = "AA"
    duration = 30

    # Cache valve flow rates
    valve_cache = {}
    for room in valve_rooms:
        valve_cache[room] = rooms[room]["flow"]

    # Pre-compute distances between all valve pairs and from start
    distance_cache = {}
    for pair in permutations(valve_rooms, 2):
        distance_cache[pair] = breadth_search(*pair, rooms) + 1  # +1 for opening valve

    for room in valve_rooms:
        distance_cache[("AA", room)] = breadth_search("AA", room, rooms) + 1

    # Find best path
    best = best_path(start, valve_cache, distance_cache, duration)

    return best


# Compute and print the answer for part 1
answer = solve_part1()
AoCUtils.print_solution(1, answer)
