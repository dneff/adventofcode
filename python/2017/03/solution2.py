"""
Advent of Code 2017 - Day 3: Spiral Memory (Part 2)

Fill the spiral memory where each square's value is the sum of all adjacent squares that have
already been filled (including diagonals). Find the first value written that is larger than
the puzzle input.

Example progression:
    147  142  133  122   59
    304    5    4    2   57
    330   10    1    1   54
    351   11   23   25   26
    362  747  806  880  931
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/3/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def get_adjacent_positions(location):
    """
    Get all 8 adjacent positions (including diagonals) for a given location.

    Args:
        location: Tuple of (x, y) coordinates

    Returns:
        List of adjacent coordinate tuples
    """
    offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    adjacent = [(location[0] + offset[0], location[1] + offset[1]) for offset in offsets]
    return adjacent


def calculate_square_value(location, filled_squares):
    """
    Calculate the value for a square based on the sum of adjacent filled squares.

    Args:
        location: Tuple of (x, y) coordinates
        filled_squares: Dictionary mapping coordinates to their values

    Returns:
        Sum of all adjacent square values
    """
    adjacent_positions = get_adjacent_positions(location)
    adjacent_values = [filled_squares[pos] for pos in adjacent_positions if pos in filled_squares]
    return sum(adjacent_values)


def main():
    """Find the first spiral value larger than the puzzle input."""
    target_value = 347991

    # Directions: Right, Up, Left, Down
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    current_dir = 0
    x, y = 0, 0
    filled_squares = {}

    # Start with square 1 at the center
    filled_squares[(x, y)] = 1

    # Move right and calculate the first non-center value
    x, y = x + directions[current_dir][0], y + directions[current_dir][1]
    filled_squares[(x, y)] = calculate_square_value((x, y), filled_squares)
    current_dir += 1

    # Continue spiraling until we find a value larger than target
    while filled_squares[(x, y)] <= target_value:
        # Check if we should turn (if the left position is unvisited)
        next_dir = (current_dir + 1) % 4
        next_loc = (x + directions[next_dir][0], y + directions[next_dir][1])
        if next_loc not in filled_squares:
            current_dir = next_dir

        # Move in the current direction
        next_loc = (x + directions[current_dir][0], y + directions[current_dir][1])
        x, y = next_loc

        # Calculate value for this square
        filled_squares[(x, y)] = calculate_square_value((x, y), filled_squares)

    AoCUtils.print_solution(2, filled_squares[(x, y)])


if __name__ == "__main__":
    main()
