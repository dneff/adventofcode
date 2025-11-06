import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/18/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402
AoCInput  # noqa: F401


def determine_tile_type(tile_pattern):
    """
    Determines if a tile is a trap (^) or safe (.) based on the pattern above it.

    A tile becomes a trap only in these cases:
    - Left and center are traps, but right is not (^^.)
    - Center and right are traps, but left is not (.^^)
    - Only left is a trap (^..)
    - Only right is a trap (..^)

    In all other cases, the tile is safe.

    Args:
        tile_pattern: A string of 3 characters representing left, center, and right tiles

    Returns:
        '^' if the new tile is a trap, '.' if safe
    """
    trap_patterns = {
        '...': '.',  # All safe -> safe
        '..^': '^',  # Only right is trap -> trap
        '.^.': '.',  # Only center is trap -> safe
        '.^^': '^',  # Center and right are traps -> trap
        '^..': '^',  # Only left is trap -> trap
        '^.^': '.',  # Left and right are traps -> safe
        '^^.': '^',  # Left and center are traps -> trap
        '^^^': '.',  # All traps -> safe
    }
    return trap_patterns[tile_pattern]


def generate_next_row(current_row):
    """
    Generates the next row of tiles based on the current row.

    Each tile in the new row is determined by looking at the three tiles above it
    (left, center, right). Tiles off the edge are treated as safe.

    Args:
        current_row: The current row of tiles as a string

    Returns:
        The next row of tiles as a string
    """
    # Pad with safe tiles on both ends to handle edge cases
    padded_row = '.' + current_row + '.'
    next_row = ''

    # For each position, look at the three tiles above (left, center, right)
    for idx in range(len(padded_row) - 2):
        tile_pattern = padded_row[idx:idx+3]
        next_row += determine_tile_type(tile_pattern)

    return next_row


def count_safe_tiles(row):
    """
    Counts the number of safe tiles (.) in a row.

    Args:
        row: A string representing a row of tiles

    Returns:
        The count of safe tiles in the row
    """
    return row.count('.')


def main():
    """
    Solves Day 18 Part 1: Like a Rogue

    Generates rows of trap and safe tiles based on the starting row pattern,
    then counts the total number of safe tiles across all rows.
    """
    # Test case from the problem description
    test = {  # noqa: F841
        'row': ".^^.^.^^^^",
        'count': 10
    }

    # Part 1: Calculate safe tiles across 40 rows
    puzzle1 = {  # noqa: F841
        'row': "^..^^.^^^..^^.^...^^^^^....^.^..^^^.^.^.^^...^.^.^.^.^^.....^.^^.^.^.^.^.^.^^..^^^^^...^.....^....^.",
        'count': 40
    }

    # Part 2: Calculate safe tiles across 400, 000 rows (used in solution2.py)
    puzzle2 = {
        'row': "^..^^.^^^..^^.^...^^^^^....^.^..^^^.^.^.^^...^.^.^.^.^^.....^.^^.^.^.^.^.^.^^..^^^^^...^.....^....^.",
        'count': 400000
    }

    # Use puzzle2 for Part 2 (400000 rows)
    active = puzzle2

    total_safe_tiles = 0
    row_count = 0

    # Start with the initial row
    current_row = active['row']
    row_count += 1

    # Count safe tiles in the first row
    total_safe_tiles += count_safe_tiles(current_row)

    # Generate subsequent rows and count safe tiles in each
    while row_count < active['count']:
        current_row = generate_next_row(current_row)
        total_safe_tiles += count_safe_tiles(current_row)
        row_count += 1

    AoCUtils.print_solution(2, total_safe_tiles)


if __name__ == "__main__":
    main()
