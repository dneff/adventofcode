"""
Advent of Code 2016 - Day 17: Two Steps Forward (Part 2)

Navigate through a 4x4 grid vault with doors controlled by MD5 hashing.
Goal: Find the LENGTH of the LONGEST path from top-left (1,1) to vault at bottom-right (4,4).

Door mechanics:
- MD5 hash of (passcode + path) determines which doors are open
- First 4 characters of hash represent Up, Down, Left, Right doors
- Characters b-f = door is open; 0-9 or 'a' = door is locked
- Once you reach the vault, you cannot pass through it (path ends)
"""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, "../../../../aoc-data/2016/17/input")
sys.path.append(os.path.join(SCRIPT_DIR, "../../"))

from aoc_helpers import AoCInput, AoCUtils

import copy
from hashlib import md5
from queue import PriorityQueue


def get_md5_hash(passcode_with_path):
    """
    Compute MD5 hash of the passcode combined with the path taken so far.

    Args:
        passcode_with_path: String combining the vault passcode and movement path

    Returns:
        MD5 hash as hexadecimal string
    """
    result = md5(passcode_with_path.encode())
    return result.hexdigest()


def get_open_doors(passcode_with_path):
    """
    Determine which doors are open based on MD5 hash.

    The first 4 characters of the hash represent doors in order: Up, Down, Left, Right.
    Characters b-f indicate an open door; any other character means locked.

    Args:
        passcode_with_path: String combining the vault passcode and movement path

    Returns:
        List of available directions ('U', 'D', 'L', 'R') for open doors
    """
    path_hash = get_md5_hash(passcode_with_path)
    unlocked_door_chars = ["b", "c", "d", "e", "f"]
    # Check first 4 hash characters against unlocked chars
    are_doors_open = [char in unlocked_door_chars for char in path_hash[:4]]
    directions = ["U", "D", "L", "R"]
    # Return only the directions where doors are open
    return [direction for direction, is_open in zip(directions, are_doors_open) if is_open]


def is_valid_room(room, grid_dimensions):
    """
    Check if room coordinates are within the valid 4x4 grid.

    Args:
        room: Tuple (x, y) representing room coordinates
        grid_dimensions: Tuple (width, height) of the grid

    Returns:
        True if room is within bounds, False otherwise
    """
    x, y = room
    if x <= 0 or x > grid_dimensions[0]:
        return False
    if y <= 0 or y > grid_dimensions[1]:
        return False
    return True


def main():
    """
    Find the longest path to the vault by exploring all possible paths.

    Unlike Part 1, we need to explore ALL paths to find the longest one.
    Key difference: paths end when reaching the vault (cannot pass through).
    We collect all path lengths that reach the vault and return the maximum.
    """
    # Movement vectors for each direction
    movement = {"U": (0, -1), "D": (0, 1), "L": (-1, 0), "R": (1, 0)}

    # Test passcodes from problem examples
    test1 = "ihgpwlah"  # shortest: DDRRRD, longest: 370
    test2 = "kglvqrro"  # shortest: DDUDRLRRUDRD, longest: 492
    test3 = "ulqzkmiv"  # shortest: DRURDRUDDLLDLUURRDULRLDUUDDDRR, longest: 830

    # The actual puzzle input passcode
    puzzle = "ioramepc"
    passcode = puzzle

    # 4x4 grid of rooms
    grid_dimensions = (4, 4)
    vault_room = (4, 4)  # Bottom-right corner

    # Start at top-left with empty path
    path = ""
    start_room = (1, 1)

    # Track seen paths to avoid redundant exploration
    seen_paths = []
    # Store lengths of all paths that reach the vault
    vault_path_lengths = set()

    # Priority queue: (path_length, [path_string, room_position])
    path_queue = PriorityQueue()
    path_queue.put((len(path), [path, copy.copy(start_room)]))

    # Explore all possible paths until queue is empty
    while not path_queue.empty():
        _, current = path_queue.get()
        path, room = current

        # Skip if we've already explored this exact path
        if path in seen_paths:
            continue
        seen_paths.append(path)

        # Determine which doors are open based on passcode + current path
        open_directions = get_open_doors(passcode + path)

        # Try each open door
        for direction in open_directions:
            # Calculate new room position
            new_room = tuple(a + b for a, b in zip(room, movement[direction]))
            new_path = path + direction

            # Check if we've reached the vault
            if new_room == vault_room:
                # Record this path length and stop this branch
                # (paths cannot pass through the vault room)
                vault_path_lengths.add(len(new_path))
                continue

            # If valid room, add to queue for further exploration
            if is_valid_room(new_room, grid_dimensions):
                path_queue.put((len(new_path), [new_path, copy.copy(new_room)]))

    # Return the length of the longest path that reaches the vault
    AoCUtils.print_solution(2, max(vault_path_lengths))


if __name__ == "__main__":
    main()
