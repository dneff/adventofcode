"""
Advent of Code 2019 - Day 20: Donut Maze

Part 1: Find the shortest path through the maze.

This maze is shaped like a donut. Portals along the inner and outer edge
of the donut can instantly teleport you from one side to the other.

In your maze, how many steps does it take to get from the open tile
marked AA to the open tile marked ZZ?
"""

import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "../../"))

from aoc_helpers import AoCInput, AoCUtils, Pathfinding  # noqa: E402
from collections import defaultdict

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, "../../../../aoc-data/2019/20/input")


def generate_maze(lines):
    """Generate maze structure from input lines.

    Args:
        lines: List of strings representing the maze grid

    Returns:
        dict: Maze adjacency graph where keys are (x, y) coordinate tuples and values
              are lists of reachable neighbor coordinates. Special keys 'AA' and 'ZZ'
              map to their respective portal entrance locations.
    """
    # Find all walkable maze positions (marked with '.')
    # Coordinates use (x, y) format where x increases rightward, y increases downward
    walkable_positions = set()
    for y, line in enumerate(lines):
        for x, cell in enumerate(line):
            if cell == ".":
                walkable_positions.add((x, y))

    # Build adjacency graph: for each walkable position, find all directly adjacent walkable neighbors
    # Only cardinal directions (up, down, left, right) are allowed - no diagonals
    maze = defaultdict(list)
    for x, y in walkable_positions:
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Left, Right, Up, Down
            neighbor = (x + dx, y + dy)
            if neighbor in walkable_positions:
                maze[(x, y)].append(neighbor)

    # Find all portals and link them in the maze
    # Portals are labeled with two uppercase letters (e.g., BC, DE, FG)
    # Each portal label appears twice in the maze - one entrance teleports to the other
    # AA and ZZ are special: they mark start and end positions (not teleporting portals)
    #
    # Portal detection strategy: scan left-to-right and top-to-bottom to find
    # the first letter of each two-letter label, then check adjacent cells
    portals = defaultdict(list)  # Maps portal label -> list of entrance positions
    for y, line in enumerate(lines):
        for x, cell in enumerate(line):
            if cell.isupper():
                # Check if there's another uppercase letter to the right (horizontal portal label)
                if x + 1 < len(line) and line[x + 1].isupper():
                    portal_label = cell + line[x + 1]
                    # The walkable entrance is either to the left of the label or to the right
                    if x - 1 >= 0 and line[x - 1] == ".":
                        portal_entrance = (x - 1, y)  # Entrance is to the left: .AB
                    elif x + 2 < len(line) and line[x + 2] == ".":
                        portal_entrance = (x + 2, y)  # Entrance is to the right: AB.
                    else:
                        continue  # No walkable tile adjacent to this label
                    portals[portal_label].append(portal_entrance)

                # Check if there's another uppercase letter below (vertical portal label)
                if y + 1 < len(lines) and lines[y + 1][x].isupper():
                    portal_label = cell + lines[y + 1][x]
                    # The walkable entrance is either above the label or below it
                    if y - 1 >= 0 and lines[y - 1][x] == ".":
                        portal_entrance = (x, y - 1)  # Entrance is above: . then A then B
                    elif y + 2 < len(lines) and lines[y + 2][x] == ".":
                        portal_entrance = (x, y + 2)  # Entrance is below: A then B then .
                    else:
                        continue  # No walkable tile adjacent to this label
                    portals[portal_label].append(portal_entrance)
    # Link portal pairs in the maze adjacency graph
    # Most portals appear twice (e.g., two "BC" labels) - walking into one teleports to the other
    # AA and ZZ are special markers for start/end and don't teleport
    for portal_label, entrance_positions in portals.items():
        if portal_label in ["AA", "ZZ"]:
            # Store start and end positions under their labels for easy access
            maze[portal_label] = entrance_positions
            continue
        elif len(entrance_positions) != 2:
            raise ValueError(
                f"Portal {portal_label} has {len(entrance_positions)} entrance(s), expected 2"
            )

        # Link the two portal entrances bidirectionally (teleportation is instant and two-way)
        entrance1, entrance2 = entrance_positions
        maze[entrance1].append(entrance2)
        maze[entrance2].append(entrance1)

    return maze


def main():
    """Find shortest path through the donut maze from AA to ZZ.

    Uses BFS to find the minimum number of steps needed to traverse the maze,
    including teleportation through portals.

    Returns:
        int: Minimum number of steps from AA to ZZ
    """
    # Read input while preserving leading spaces (important for portal detection)
    lines = AoCInput.read_lines(INPUT_FILE, preserve_leading_space=True)
    maze = generate_maze(lines)

    # Extract start and end positions from the maze
    start_position = maze["AA"][0]
    end_position = maze["ZZ"][0]

    print(
        f"Maze has {len(maze)} locations.\n"
        f"Start location: {start_position}, End location: {end_position}"
    )

    # Use BFS to find shortest path (BFS guarantees shortest path in unweighted graphs)
    # The get_neighbors function returns all reachable positions from a given position
    # This includes both adjacent walkable tiles AND portal teleportation destinations
    steps_to_end = Pathfinding.bfs_distance(
        start_position, end_position, get_neighbors=lambda position: maze[position]
    )
    return steps_to_end


if __name__ == "__main__":
    answer = main()
    AoCUtils.print_solution(1, answer)
