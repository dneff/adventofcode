"""
Advent of Code 2018 - Day 22: Mode Maze (Part 2)
https://adventofcode.com/2018/day/22

Part 2

In this part, you need to determine the minimum time required to reach the target coordinates
from the mouth of the cave, considering the allowed tools and region types.

The cave system consists of regions at integer coordinates, each with:
- Geologic Index: Calculated based on position
- Erosion Level: (geologic index + depth) % 20183
- Region Type: erosion level % 3 (0=rocky, 1=wet, 2=narrow)
- Risk Level: Same as region type (0, 1, or 2)
"""

import os
import sys
from heapq import heappop, heappush

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, "../../../../aoc-data/2018/22/input")
sys.path.append(os.path.join(SCRIPT_DIR, "../../"))

from aoc_helpers import AoCInput, AoCUtils

# Parse input: cave depth and target coordinates
input_lines = AoCInput.read_lines(INPUT_FILE)
cave_depth = int(input_lines[0].split(": ")[1])
target_x, target_y = map(int, input_lines[1].split(": ")[1].split(","))
target_coords = (target_x, target_y)


def calculate_erosion_level(erosion_cache, x, y):
    """
    Calculate the erosion level for a cave region at coordinates (x, y).

    Erosion level calculation:
    1. Determine geologic index based on position:
       - Origin (0,0) and target: geologic index = 0
       - Y=0 (top edge): geologic index = X * 16807
       - X=0 (left edge): geologic index = Y * 48271
       - Other regions: geologic index = erosion_left * erosion_above
    2. Erosion level = (geologic index + cave_depth) % 20183

    Args:
        erosion_cache: Dictionary caching previously calculated erosion levels
        x, y: Coordinates of the region

    Returns:
        int: The erosion level for the region at (x, y)
    """
    # Return cached value if already calculated
    if (x, y) in erosion_cache:
        return erosion_cache[(x, y)]

    # Calculate geologic index based on position
    if (x, y) == (0, 0) or (x, y) == target_coords:
        # Mouth of cave and target have geologic index 0
        geologic_index = 0
    elif y == 0:
        # Top edge: geologic index = X * 16807
        geologic_index = x * 16807
    elif x == 0:
        # Left edge: geologic index = Y * 48271
        geologic_index = y * 48271
    else:
        # Interior regions: geologic index = erosion_left * erosion_above
        erosion_left = calculate_erosion_level(erosion_cache, x - 1, y)
        erosion_above = calculate_erosion_level(erosion_cache, x, y - 1)
        geologic_index = erosion_left * erosion_above

    # Calculate erosion level from geologic index
    erosion_level = (geologic_index + cave_depth) % 20183

    # Cache the result
    erosion_cache[(x, y)] = erosion_level

    return erosion_level


# Generate the region map with types based on erosion levels
# Region types: 0=rocky, 1=wet, 2=narrow
region_map = {}

# Cache for erosion levels to avoid recalculation
erosion_cache = {}

# Extra buffer beyond target to ensure we can explore alternative paths
# that might go around the target to reach it faster
SEARCH_BUFFER = 40

for y in range(0, target_y + SEARCH_BUFFER):
    for x in range(0, target_x + SEARCH_BUFFER):
        erosion_level = calculate_erosion_level(erosion_cache, x, y)
        region_type = erosion_level % 3  # 0=rocky, 1=wet, 2=narrow
        region_map[(x, y)] = region_type


def get_neighbors(position):
    """
    Get all valid adjacent positions (up, down, left, right) from the given position.

    Args:
        position: Tuple (x, y) representing current coordinates

    Returns:
        List of valid neighboring positions that exist in the region map
    """
    x, y = position
    neighbors = []
    # Check all 4 cardinal directions (no diagonal movement allowed)
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        neighbor_x, neighbor_y = x + dx, y + dy
        # Only include neighbors that are within our pre-calculated region map
        if (neighbor_x, neighbor_y) in region_map:
            neighbors.append((neighbor_x, neighbor_y))
    return neighbors


def get_allowed_tools(region_type):
    """
    Determine which tools can be used in a given region type.

    Tool constraints by region:
    - Rocky (0): Can use climbing gear or torch (cannot use neither - would slip)
    - Wet (1): Can use climbing gear or neither (cannot use torch - would get wet)
    - Narrow (2): Can use torch or neither (cannot use climbing gear - too bulky)

    Tool encoding: 0=neither, 1=climbing gear, 2=torch

    Args:
        region_type: Integer 0 (rocky), 1 (wet), or 2 (narrow)

    Returns:
        Set of allowed tool IDs for the region type
    """
    if region_type == 0:  # Rocky region
        return {1, 2}  # Climbing gear or Torch
    elif region_type == 1:  # Wet region
        return {0, 1}  # Neither or Climbing gear
    else:  # Narrow region (type 2)
        return {0, 2}  # Neither or Torch


# ========== Dijkstra's Algorithm for Shortest Path ==========
# State representation: (x, y, tool) where tool affects movement costs
# - Moving to adjacent cell: 1 minute
# - Switching tools: 7 minutes
# - Must have correct tool for each region type
# - Goal: Reach target with torch equipped

# Tool encoding constants
TOOL_NEITHER = 0
TOOL_CLIMBING_GEAR = 1
TOOL_TORCH = 2

# Time costs
MOVE_TIME = 1  # Minutes to move to adjacent region
TOOL_SWITCH_TIME = 7  # Minutes to switch tools

# Starting conditions
starting_position = (0, 0)
starting_tool = TOOL_TORCH  # We start with torch equipped

# Track the best time found to reach target with torch
best_time_to_target = float('inf')

# Priority queue: (elapsed_time, (x, y, tool))
# Using min-heap to always process the state with lowest cost first
priority_queue = [(0, (starting_position[0], starting_position[1], starting_tool))]

# Distance map: tracks minimum time to reach each state (x, y, tool)
min_time_to_state = {(starting_position[0], starting_position[1], starting_tool): 0}

while priority_queue:
    # Extract the state with minimum time from the priority queue
    current_time, current_state = heappop(priority_queue)
    current_x, current_y, current_tool = current_state

    # Pruning: Skip this state if we've already found a better complete path
    if current_time > best_time_to_target:
        continue

    # Check if we've reached the goal: target position with torch equipped
    if current_state == (target_x, target_y, TOOL_TORCH):
        best_time_to_target = current_time
        continue  # Keep searching for potentially better paths

    # Skip if we've already found a better path to this exact state
    if current_time > min_time_to_state.get(current_state, float('inf')):
        continue

    # Explore all adjacent positions (up, down, left, right)
    for neighbor_pos in get_neighbors((current_x, current_y)):
        neighbor_x, neighbor_y = neighbor_pos
        neighbor_region_type = region_map[neighbor_pos]
        allowed_tools_in_neighbor = get_allowed_tools(neighbor_region_type)

        # Check if current tool is valid in the neighbor region
        if current_tool in allowed_tools_in_neighbor:
            # Can move directly without tool change
            new_time = current_time + MOVE_TIME
            neighbor_state = (neighbor_x, neighbor_y, current_tool)

            # Only update if this is a better path to this state
            if new_time < min_time_to_state.get(neighbor_state, float('inf')):
                min_time_to_state[neighbor_state] = new_time
                heappush(priority_queue, (new_time, neighbor_state))
        else:
            # Current tool is NOT valid in neighbor - must switch tools first
            # Cost: MOVE_TIME (1 min) + TOOL_SWITCH_TIME (7 min) = 8 minutes total
            new_time = current_time + MOVE_TIME + TOOL_SWITCH_TIME

            # Try all valid tools in the neighbor region (except current one)
            for valid_tool in allowed_tools_in_neighbor:
                if valid_tool != current_tool:
                    neighbor_state = (neighbor_x, neighbor_y, valid_tool)

                    # Only update if this is a better path to this state
                    if new_time < min_time_to_state.get(neighbor_state, float('inf')):
                        min_time_to_state[neighbor_state] = new_time
                        heappush(priority_queue, (new_time, neighbor_state))

# Print the minimum time required to reach the target
AoCUtils.print_solution(2, best_time_to_target)