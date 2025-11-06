"""
Advent of Code 2016 - Day 24: Air Duct Spelunking (Part 2)

Problem: Same as Part 1, but with an additional requirement: after visiting all
numbered locations, the robot must return to its starting position (location 0).

The map consists of:
- '0': starting position (must return here)
- '1'-'7': numbered locations the robot must visit
- '#': walls (impassable)
- '.': open passages (passable)

Solution approach:
1. Parse the air duct map and identify all numbered locations
2. Use A* pathfinding to calculate distances between all location pairs
3. Try all permutations of visiting orders (starting from 0, ending at 0)
4. Return the shortest total round-trip path length
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/24/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

from queue import PriorityQueue  # noqa: E402
from itertools import permutations  # noqa: E402


class AirDuctMap():
    """Represents the air duct system with numbered locations and open passages."""

    def __init__(self):
        self.open_passages = set()  # Set of (row, col) coordinates that are passable
        self.numbered_locations = {}  # Maps location number to (row, col) coordinate

    def remove_dead_ends(self):
        """
        Optimization: Remove dead-end passages that don't lead to numbered locations.
        This reduces the search space for pathfinding without affecting the result.
        """
        max_row = max([x[0] for x in self.open_passages])
        max_col = max([x[1] for x in self.open_passages])
        dead_ends_removed = 1
        while dead_ends_removed > 0:
            dead_ends_removed = 0
            for r in range(max_row + 1):
                for c in range(max_col + 1):
                    # If this passage has only 1 or fewer neighbors and isn't a numbered location
                    if (r, c) in self.open_passages and (r, c) not in self.numbered_locations.values():
                        if len(self.get_adjacent_passages((r, c))) <= 1:
                            self.open_passages.remove((r, c))
                            dead_ends_removed += 1

    def display(self):
        """Debug method to visualize the air duct map."""
        max_row = max([x[0] for x in self.open_passages])
        max_col = max([x[1] for x in self.open_passages])
        for r in range(max_row + 1):
            row = ''
            for c in range(max_col + 1):
                if (r, c) in self.numbered_locations.values():
                    # Show the actual location number
                    location_num = [k for k, v in self.numbered_locations.items() if v == (r, c)][0]
                    row += str(location_num)
                elif (r, c) in self.open_passages:
                    row += '.'
                else:
                    row += ' '
            print(row)

    def add_open_passage(self, position):
        """Mark a position as an open passage (not a wall)."""
        if position not in self.open_passages:
            self.open_passages.add(position)

    def add_numbered_location(self, location_number, position):
        """Add a numbered location that the robot must visit."""
        self.numbered_locations[location_number] = position
        self.add_open_passage(position)

    def get_adjacent_passages(self, position):
        """
        Get all adjacent open passages (up, down, left, right).
        The robot cannot move diagonally.
        """
        adjacent = []
        row, col = position
        # Check all four cardinal directions
        candidates = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
        for candidate in candidates:
            if candidate in self.open_passages:
                adjacent.append(candidate)
        return adjacent

    def manhattan_distance(self, pos_a, pos_b):
        """Calculate Manhattan distance (heuristic for A* pathfinding)."""
        return abs(pos_a[0] - pos_b[0]) + abs(pos_a[1] - pos_b[1])

    def find_shortest_path_length(self, start_pos, end_pos):
        """
        Use A* pathfinding to find the shortest path length between two positions.
        Returns the number of steps required.
        """
        visited = set()
        priority_queue = PriorityQueue()

        # Priority queue contains tuples of (priority_score, (current_position, steps_taken))
        priority_queue.put((0, (start_pos, 0)))

        while not priority_queue.empty():
            _, (current_pos, steps) = priority_queue.get()

            if current_pos in visited:
                continue

            visited.add(current_pos)
            next_steps = steps + 1

            # Explore all adjacent passages
            for adjacent_pos in self.get_adjacent_passages(current_pos):
                if adjacent_pos not in visited:
                    # Found the destination
                    if adjacent_pos == end_pos:
                        return next_steps

                    # A* heuristic: distance to goal + steps taken so far
                    priority_score = self.manhattan_distance(adjacent_pos, end_pos) + next_steps
                    priority_queue.put((priority_score, (adjacent_pos, next_steps)))

        return None  # No path found


def main():  # noqa: C901
    """
    Main solution for Part 2:
    1. Parse the air duct map
    2. Calculate pairwise distances between all numbered locations
    3. Find the shortest ROUND-TRIP route: start at 0, visit all locations, return to 0
    """

    # Parse the air duct map from input
    air_ducts = AirDuctMap()
    for row, line in enumerate(AoCInput.read_lines(INPUT_FILE)):
        for col, char in enumerate(line):
            if char == '.':
                air_ducts.add_open_passage((row, col))
            if char.isdigit():
                air_ducts.add_numbered_location(int(char), (row, col))

    # Optimize the map by removing dead ends
    air_ducts.remove_dead_ends()

    # Calculate distances between all pairs of numbered locations
    location_distances = {}
    for start_num in air_ducts.numbered_locations.keys():
        for end_num in air_ducts.numbered_locations.keys():
            if start_num == end_num:
                continue
            if (start_num, end_num) in location_distances:
                continue

            # Only calculate path if Manhattan distance is reasonable
            manhattan_dist = air_ducts.manhattan_distance(
                air_ducts.numbered_locations[start_num],
                air_ducts.numbered_locations[end_num]
            )
            if manhattan_dist <= 140:
                path_length = air_ducts.find_shortest_path_length(
                    air_ducts.numbered_locations[start_num],
                    air_ducts.numbered_locations[end_num]
                )
                # Store distance for both directions (symmetric)
                location_distances[(start_num, end_num)] = path_length
                location_distances[(end_num, start_num)] = path_length

    # Try all permutations of visiting locations 1-7, starting and ending at 0
    valid_routes = {}
    for visit_order in permutations(range(1, 8)):
        # Build the full ROUND-TRIP route: start at 0, visit all locations, return to 0
        full_route = [0] + list(visit_order) + [0]
        # Create pairs of consecutive locations to visit
        route_segments = list(zip(full_route[:-1], full_route[1:]))

        # Calculate total distance for this round-trip route
        total_distance = 0
        for segment in route_segments:
            if segment in location_distances:
                total_distance += location_distances[segment]
            else:
                # Invalid route (missing connection)
                total_distance = 0
                break

        if total_distance > 0:
            valid_routes[total_distance] = route_segments

    # The answer is the minimum distance among all valid round-trip routes
    shortest_roundtrip_length = min(valid_routes.keys())
    AoCUtils.print_solution(2, shortest_roundtrip_length)


if __name__ == "__main__":
    main()
