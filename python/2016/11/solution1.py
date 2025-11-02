"""
Advent of Code 2016 Day 11: Radioisotope Thermoelectric Generators

Problem: Move all RTGs (generators) and microchips to the 4th floor using an elevator.
The elevator can carry 1-2 items and requires at least 1 item to move.

Safety constraint: A microchip will be fried if it's on the same floor as another RTG
unless its matching RTG is also present to provide shielding.

Solution approach: A* pathfinding algorithm
- State: positions of all items (microchips and generators) + elevator floor
- Goal: all items on the top floor
- Heuristic: sum of (top_floor - item_floor) for all items
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/11/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
import copy
from queue import PriorityQueue
from collections import defaultdict
from itertools import combinations


def parse_floor_items(floor_description):
    """
    Parse a floor description to extract RTGs and microchips.

    Example: "The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip."
    Returns: ['hydrogen.microchip', 'lithium.microchip']
    """
    items = []
    for i, word in enumerate(floor_description.replace(".", "").replace(",", "").split()):
        if word in ['microchip', 'generator']:
            # Extract element name from the previous word (e.g., "hydrogen-compatible" -> "hydrogen")
            element = floor_description.split()[i-1].split("-")[0]
            item = element + "." + word
            items.append(item)
    return items

def parse_initial_state(filename):
    """
    Parse the input file to create the initial state of the facility.

    Returns:
        tuple: (items, num_floors, elevator_floor)
        - items: list of [microchip_floor, generator_floor] pairs for each element
        - num_floors: total number of floors in the facility
        - elevator_floor: starting floor of the elevator (always 1)

    Note: Items are represented as pairs [chip_floor, rtg_floor] where each element
    has its microchip position at index 0 and RTG position at index 1.
    """
    num_floors = 0
    # Track each element's [microchip_floor, rtg_floor]
    element_positions = defaultdict(lambda: [0] * 2)

    lines = AoCInput.read_lines(filename)
    for floor_num, floor_description in enumerate(lines):
        num_floors += 1
        for item in parse_floor_items(floor_description):
            element, item_type = item.split('.')
            if item_type == 'generator':
                # RTG position is at index 1
                element_positions[element][1] = floor_num + 1
            else:  # microchip
                # Microchip position is at index 0
                element_positions[element][0] = floor_num + 1

    # Sort the items for consistent state representation
    items = sorted([list(positions) for positions in element_positions.values()])
    elevator_floor = 1  # Elevator starts on floor 1

    return items, num_floors, elevator_floor

def is_safe_configuration(items):
    """
    Check if the current configuration is safe (no microchips will be fried).

    Safety rule: A microchip is safe if:
    1. It's on the same floor as its matching RTG, OR
    2. There are no other RTGs on its floor

    Args:
        items: list of [microchip_floor, rtg_floor] pairs

    Returns:
        bool: True if configuration is safe, False if any chip would be fried
    """
    # Get all floors that have RTGs
    rtg_floors = [rtg_floor for chip_floor, rtg_floor in items]

    for chip_floor, rtg_floor in items:
        # If chip is with its own RTG, it's safe
        if chip_floor == rtg_floor:
            continue
        # If chip is on a floor with any other RTG, it will be fried
        if chip_floor in rtg_floors:
            return False

    return True

def calculate_heuristic(items, num_floors):
    """
    Calculate heuristic for A* search: distance to goal state.

    The goal is to have all items on the top floor. This heuristic sums
    the distance each item needs to travel to reach the top floor.

    Args:
        items: list of [microchip_floor, rtg_floor] pairs
        num_floors: total number of floors (top floor number)

    Returns:
        int: sum of (top_floor - item_floor) for all items
    """
    all_floors = []
    for chip_floor, rtg_floor in items:
        all_floors.extend([chip_floor, rtg_floor])

    # Calculate sum of distances: for each item, (top_floor - current_floor)
    # This is equivalent to: (top_floor * num_items) - sum(all_floors)
    distance = num_floors * len(all_floors) - sum(all_floors)
    return distance

def calculate_a_star_score(state, num_floors):
    """
    Calculate the A* score for prioritizing states to explore.

    A* score = g(n) + h(n) where:
    - g(n) = actual cost from start (number of moves taken)
    - h(n) = heuristic estimate of cost to goal (distance to complete)

    Args:
        state: tuple of (items, elevator_floor, num_moves)
        num_floors: total number of floors

    Returns:
        int: A* score for this state (lower is better)
    """
    items, elevator_floor, num_moves = state

    # g(n): actual cost from start
    moves_taken = num_moves

    # h(n): heuristic estimate to goal
    estimated_moves_remaining = calculate_heuristic(items, num_floors)

    score = moves_taken + estimated_moves_remaining
    return score

def find_next_possible_states(state, num_floors):
    """
    Generate all valid next states from the current state.

    The elevator can move up or down one floor, carrying 1-2 items.
    Valid moves:
    1. Elevator must carry at least 1 item (and at most 2)
    2. Resulting configuration must be safe (no chips fried)
    3. Cannot move below the lowest floor with items (optimization)
    4. Cannot move above the top floor

    Args:
        state: tuple of (items, elevator_floor, num_moves)
        num_floors: total number of floors

    Returns:
        list: all valid next states as (items, elevator_floor, num_moves) tuples
    """
    next_states = []
    items, elevator_floor, num_moves = state

    # Find all item floors to determine minimum floor with items
    all_item_floors = []
    for chip_floor, rtg_floor in items:
        all_item_floors.extend([chip_floor, rtg_floor])
    min_occupied_floor = min(all_item_floors)

    # Find all items on the current elevator floor
    items_on_elevator_floor = []
    for element_idx, (chip_floor, rtg_floor) in enumerate(items):
        if chip_floor == elevator_floor:
            items_on_elevator_floor.append([element_idx, 0])  # [element_index, 0=chip]
        if rtg_floor == elevator_floor:
            items_on_elevator_floor.append([element_idx, 1])  # [element_index, 1=rtg]

    # Generate all combinations of 1-2 items to move
    possible_loads = []
    possible_loads.extend(combinations(items_on_elevator_floor, 1))
    possible_loads.extend(combinations(items_on_elevator_floor, 2))

    # Try moving up (if not at top floor)
    if elevator_floor < num_floors:
        for load in possible_loads:
            new_items = copy.deepcopy(items)
            for element_idx, item_type in load:
                new_items[element_idx][item_type] = elevator_floor + 1
            new_items.sort()
            if is_safe_configuration(new_items):
                next_states.append((new_items, elevator_floor + 1, num_moves + 1))

    # Try moving down (if above lowest occupied floor)
    if elevator_floor > min_occupied_floor:
        for load in possible_loads:
            new_items = copy.deepcopy(items)
            for element_idx, item_type in load:
                new_items[element_idx][item_type] = elevator_floor - 1
            new_items.sort()
            if is_safe_configuration(new_items):
                next_states.append((new_items, elevator_floor - 1, num_moves + 1))

    return next_states



def main():
    """
    Solve the Radioisotope Testing Facility puzzle using A* pathfinding.

    Uses A* algorithm to find the minimum number of elevator moves needed to
    transport all RTGs and microchips to the top floor while maintaining safety.
    """
    # Track visited states to avoid revisiting (items, elevator_floor)
    visited_states = set()

    # Priority queue for A* search: stores (priority_score, state)
    priority_queue = PriorityQueue()

    # Parse the initial facility configuration
    items, num_floors, elevator_floor = parse_initial_state(INPUT_FILE)

    # Initialize search with starting state (items, elevator_floor, num_moves)
    num_moves = 0
    start_state = (items, elevator_floor, num_moves)
    start_score = calculate_a_star_score(start_state, num_floors)
    priority_queue.put((start_score, start_state))

    # A* search loop
    while not priority_queue.empty():
        # Get the most promising state to explore
        _, current_state = priority_queue.get()
        current_items, current_elevator, current_moves = current_state

        # Skip if we've already visited this configuration
        state_signature = (tuple(map(tuple, current_items)), current_elevator)
        if state_signature in visited_states:
            continue
        visited_states.add(state_signature)

        # Check if we've reached the goal (all items on top floor)
        if calculate_heuristic(current_items, num_floors) == 0:
            AoCUtils.print_solution(1, current_moves)
            return

        # Generate and evaluate all possible next states
        next_states = find_next_possible_states(current_state, num_floors)

        for next_state in next_states:
            next_items, next_elevator, next_moves = next_state

            # Skip if we've already visited this configuration
            next_signature = (tuple(map(tuple, next_items)), next_elevator)
            if next_signature in visited_states:
                continue

            # Add to priority queue with A* score
            next_score = calculate_a_star_score(next_state, num_floors)
            priority_queue.put((next_score, next_state))


if __name__ == "__main__":
    main()