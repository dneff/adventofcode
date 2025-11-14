"""
Advent of Code 2019 - Day 20: Donut Maze

Part 2: Find the shortest path through the maze.

The marked connections in the maze aren't portals: they physically 
connect to a larger or smaller copy of the maze. Specifically, the 
labeled tiles around the inside edge actually connect to a smaller 
copy of the same maze, and the smaller copy's inner labeled tiles 
connect to yet a smaller copy, and so on.

When you enter the maze, you are at the outermost level; when at 
the outermost level, only the outer labels AA and ZZ function (as 
the start and end, respectively); all other outer labeled tiles are 
effectively walls. At any other level, AA and ZZ count as walls, 
but the other outer labeled tiles bring you one level outward.

Your goal is to find a path through the maze that brings you back 
to ZZ at the outermost level of the maze.
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
    """Generate maze structure from input lines for recursive depth navigation.

    In Part 2, the maze has recursive depth levels. Inner portals go deeper (increase depth),
    while outer portals go shallower (decrease depth). This function separates normal walking
    from portal teleportation for depth tracking.

    Args:
        lines: List of strings representing the maze grid

    Returns:
        tuple: (maze, portal_map, start, end) where:
            - maze: dict with (x, y) coordinate tuples as keys, values are lists of
                   adjacent walkable coordinates (no portal teleportation)
            - portal_map: dict mapping portal entrance (x, y) -> (destination, is_inner)
                         where is_inner is True for inner portals, False for outer
            - start: (x, y) coordinate of AA entrance
            - end: (x, y) coordinate of ZZ entrance
    """
    # Find all walkable maze positions (marked with '.')
    # Coordinates use (x, y) format where x increases rightward, y increases downward
    walkable_positions = set()
    for y, line in enumerate(lines):
        for x, cell in enumerate(line):
            if cell == ".":
                walkable_positions.add((x, y))

    # Build adjacency graph for normal walking (no portal teleportation)
    # Only cardinal directions (up, down, left, right) are allowed - no diagonals
    maze = defaultdict(list)
    for x, y in walkable_positions:
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Left, Right, Up, Down
            neighbor = (x + dx, y + dy)
            if neighbor in walkable_positions:
                maze[(x, y)].append(neighbor)

    # Find all portals and classify them as inner or outer
    # Portals are labeled with two uppercase letters (e.g., BC, DE, FG)
    # Each portal label appears twice in the maze - one entrance teleports to the other
    # AA and ZZ are special: they mark start and end positions (not teleporting portals)
    #
    # Part 2 distinction: portals can be "inner" (near center) or "outer" (near edges)
    # - Outer portals are close to the edges of the grid (within 2-3 tiles)
    # - Inner portals are in the middle area (the donut hole)
    # - Inner portals go DOWN one recursive level (depth + 1)
    # - Outer portals go UP one recursive level (depth - 1)
    #
    # Portal detection strategy: scan left-to-right and top-to-bottom to find
    # the first letter of each two-letter label, then check adjacent cells
    width = max(len(line) for line in lines)
    height = len(lines)

    portals = defaultdict(list)  # Maps portal label -> list of entrance positions
    portal_types = {}  # Maps portal entrance position -> True (inner) or False (outer)
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

                    # Determine if this portal is inner (near center) or outer (near edge)
                    # Outer portals are within 2-3 tiles of the grid boundaries
                    px, py = portal_entrance
                    is_outer = px <= 2 or px >= width - 3 or py <= 2 or py >= height - 3
                    portal_types[portal_entrance] = not is_outer  # True = inner, False = outer

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

                    # Determine if this portal is inner (near center) or outer (near edge)
                    # Outer portals are within 2-3 tiles of the grid boundaries
                    px, py = portal_entrance
                    is_outer = px <= 2 or px >= width - 3 or py <= 2 or py >= height - 3
                    portal_types[portal_entrance] = not is_outer  # True = inner, False = outer

    # Create portal map for teleportation (separate from normal walking adjacency)
    # Format: entrance position -> (destination position, is_inner_portal)
    # This separation allows tracking depth changes when using portals
    portal_map = {}
    start_position = None
    end_position = None

    for portal_label, entrance_positions in portals.items():
        if portal_label == "AA":
            # AA is the starting position (not a teleporting portal)
            start_position = entrance_positions[0]
            continue
        elif portal_label == "ZZ":
            # ZZ is the ending position (not a teleporting portal)
            end_position = entrance_positions[0]
            continue
        elif len(entrance_positions) != 2:
            raise ValueError(
                f"Portal {portal_label} has {len(entrance_positions)} entrance(s), expected 2"
            )

        # Link the two portal entrances bidirectionally with their inner/outer classification
        entrance1, entrance2 = entrance_positions
        portal_map[entrance1] = (entrance2, portal_types[entrance1])
        portal_map[entrance2] = (entrance1, portal_types[entrance2])

    return maze, portal_map, start_position, end_position


def main():
    """Find shortest path through the recursive donut maze from AA to ZZ.

    In Part 2, the maze has recursive depth levels. The state is now (position, depth)
    where depth represents how many levels deep we are in the recursion.

    Rules:
    - Start at AA with depth 0
    - Must reach ZZ at depth 0
    - Inner portals increase depth (go deeper into recursion)
    - Outer portals decrease depth (go back up) but only if depth > 0
    - At depth 0, only AA and ZZ work; other outer portals are walls
    - At depth > 0, AA and ZZ are walls (can't walk on them)

    Returns:
        int: Minimum number of steps from (AA, depth=0) to (ZZ, depth=0)
    """
    # Read input while preserving leading spaces (important for portal detection)
    lines = AoCInput.read_lines(INPUT_FILE, preserve_leading_space=True)
    maze, portal_map, start_position, end_position = generate_maze(lines)

    def get_neighbors(state):
        """Get all reachable states from the current state.

        Args:
            state: Tuple of ((x, y), depth) representing position and recursion level

        Returns:
            list: List of reachable (position, depth) tuples
        """
        position, depth = state
        neighbors = []

        # Option 1: Walk to adjacent tiles (normal movement, stays at same depth)
        for adjacent_position in maze[position]:
            # Special rule: At depth > 0, AA and ZZ become walls (can't walk on them)
            # This prevents accidentally stepping on start/end positions in deeper levels
            if depth > 0 and (adjacent_position == start_position or adjacent_position == end_position):
                continue
            neighbors.append((adjacent_position, depth))

        # Option 2: Use a portal (if standing on one) to teleport to paired location
        if position in portal_map:
            destination_position, is_inner_portal = portal_map[position]

            if is_inner_portal:
                # Inner portals go one level deeper (toward the center of the recursion)
                # No depth limit - can go arbitrarily deep
                neighbors.append((destination_position, depth + 1))
            else:
                # Outer portals go one level up (toward the surface)
                # Only allowed if depth > 0; at depth 0, outer portals are walls
                if depth > 0:
                    neighbors.append((destination_position, depth - 1))

        return neighbors

    # Start at AA with depth 0, goal is to reach ZZ at depth 0
    start_state = (start_position, 0)
    end_state = (end_position, 0)

    # Use BFS to find shortest path (BFS guarantees shortest path in unweighted graphs)
    steps_to_end = Pathfinding.bfs_distance(start_state, end_state, get_neighbors)
    return steps_to_end


if __name__ == "__main__":
    answer = main()
    AoCUtils.print_solution(2, answer)
