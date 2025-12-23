"""
Advent of Code 2019 - Day 24: Planet of Discord
https://adventofcode.com/2019/day/24


Eris isn't a very large place; a scan of the entire area fits into a 5x5 grid 
(your puzzle input). The scan shows bugs (#) and empty spaces (.).

Each minute, The bugs live and die based on the number of bugs in the four 
adjacent tiles:

A bug dies (becoming an empty space) unless there is exactly one bug adjacent to it.
An empty space becomes infested with a bug if exactly one or two bugs are adjacent to it.
Otherwise, a bug or empty space remains the same.

Part 2

This 5x5 grid is only one level in an infinite number of recursion levels. The tile in the 
middle of the grid is actually another 5x5 grid, the grid in your scan is contained as the 
middle tile of a larger 5x5 grid, and so on.

Starting with your scan, how many bugs are present after 200 minutes?

STRATEGY:
We no longer need to calculate the biodiversity rating, we can just simulate the bug life cycle.
Adjust the adjacent tiles to account for the fact that we are now in a 5x5 grid that is contained in a larger 5x5 grid, and so on.
Adjacent tiles are still a constant relationship, but we need to include depth in the calculation.
Adjacent values are now a tuple of (x, y, z).



"""

import os
import sys


# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "../../"))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, "../../../../aoc-data/2019/24/input")


def get_adjacent_tiles(x, y, z):
    """Get adjacent tiles for position (x, y, z) in a 5x5 recursive grid."""
    adj = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Center tile (2,2) is the recursive level - it has no adjacent tiles
    if x == 2 and y == 2:
        return []
    
    # Check each direction
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        
        # If neighbor would be the center, it connects to inner level
        if nx == 2 and ny == 2:
            # Connect to the entire edge of the inner level (z-1)
            # When going into center, you see the inner level from the opposite side
            if dx == -1:  # Coming from east into center -> inner level's east edge
                adj.extend([(4, i, z-1) for i in range(5)])
            elif dx == 1:  # Coming from west into center -> inner level's west edge
                adj.extend([(0, i, z-1) for i in range(5)])
            elif dy == -1:  # Going north into center -> see inner level's south edge (from above)
                adj.extend([(i, 4, z-1) for i in range(5)])
            elif dy == 1:  # Going south into center -> see inner level's north edge (from below)
                adj.extend([(i, 0, z-1) for i in range(5)])
        # If neighbor is within bounds, add it
        elif 0 <= nx < 5 and 0 <= ny < 5:
            adj.append((nx, ny, z))
        # If neighbor is outside bounds, connect to outer level
        else:
            # Map edge positions to outer level connections
            if nx < 0:  # West edge -> outer level's position west of center
                adj.append((1, 2, z+1))
            elif nx >= 5:  # East edge -> outer level's position east of center
                adj.append((3, 2, z+1))
            elif ny < 0:  # North edge -> outer level's position north of center
                adj.append((2, 1, z+1))
            elif ny >= 5:  # South edge -> outer level's position south of center
                adj.append((2, 3, z+1))
    
    return adj


def simulate_recursive_bugs(tiles_lines, minutes, verbose=False):
    """Run the recursive bug simulation for a number of minutes."""
    current_bugs = set()
    for y, row in enumerate(tiles_lines):
        for x, tile in enumerate(row):
            # Skip the center tile (2,2) - represents the inner level
            if x == 2 and y == 2:
                continue
            if tile == '#':
                current_bugs.add((x, y, 0))

    minute_count = 0
    while minute_count < minutes:
        new_bugs = set()
        # Track tiles that can change: bugs and their neighbors
        tiles_to_check = set(current_bugs)
        for bug in current_bugs:
            tiles_to_check.update(get_adjacent_tiles(*bug))

        for tile in tiles_to_check:
            adjacent_tiles = get_adjacent_tiles(*tile)
            bug_count = sum(1 for adj_tile in adjacent_tiles if adj_tile in current_bugs)

            if tile in current_bugs:
                # A bug survives only with exactly one adjacent bug
                if bug_count == 1:
                    new_bugs.add(tile)
            else:
                # Empty becomes bug with 1 or 2 adjacent bugs
                if bug_count in (1, 2):
                    new_bugs.add(tile)

        current_bugs = new_bugs
        minute_count += 1
        if verbose:
            print(f"Minute {minute_count}: {len(current_bugs)} bugs")

    return current_bugs


if __name__ == "__main__":
    tiles = AoCInput.read_lines(INPUT_FILE)
    final_bugs = simulate_recursive_bugs(tiles, minutes=200)
    AoCUtils.print_solution(2, len(final_bugs))



