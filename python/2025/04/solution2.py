"""
Advent of Code 2025 - Day 4: Printing Department
https://adventofcode.com/2025/day/4

Part Two

The forklifts can only access a roll of paper if there are fewer than 
four rolls of paper in the eight adjacent positions. If you can figure 
out which rolls of paper the forklifts can access, they'll spend less 
time looking and more time breaking down the wall to the cafeteria.

In this example, there are 13 rolls of paper that can be accessed by 
a forklift (marked with x):

..xx.xx@x.
x@@.@.@.@@
@@@@@.x.@@
@.@@@@..@.
x@.@@@@.@x
.@@@@@@@.@
.@.@.@.@@@
x.@@@.@@@@
.@@@@@@@@.
x.x.@@@.x.

Once a roll of paper can be accessed by a forklift, it can be removed. Once 
a roll of paper is removed, the forklifts might be able to access more rolls 
of paper, which they might also be able to remove. How many total rolls of 
paper could the Elves remove if they keep repeating this process?
"""

import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2025/4/input')

def count_adjacent_paper_rolls(position, all_roll_positions):
    """
    Count how many paper rolls are adjacent to the given position.
    
    Args:
        position: Tuple (x, y) representing the position to check
        all_roll_positions: Set of all positions containing paper rolls
    
    Returns:
        Number of adjacent paper rolls (0-8)
    """
    x, y = position
    # All 8 directions: diagonals and cardinal directions
    directions = [(-1, -1), (0, -1), (1, -1),
                  (-1, 0),          (1, 0),
                  (-1, 1),  (0, 1),  (1, 1)]
    
    # Count how many adjacent positions contain paper rolls (O(1) lookup with set)
    return sum(1 for dx, dy in directions if (x + dx, y + dy) in all_roll_positions)

# Read the warehouse diagram from input file
warehouse_diagram = AoCInput.read_lines(INPUT_FILE)

# Parse the diagram to find all paper roll positions (marked with '@')
# Use set comprehension for O(1) lookups instead of tuple with O(n) lookups
paper_roll_positions = {
    (x, y)
    for y, line in enumerate(warehouse_diagram)
    for x, char in enumerate(line)
    if char == '@'
}

# Track initial count before removal process begins
initial_roll_count = len(paper_roll_positions)

# Iteratively remove accessible paper rolls until none can be removed
while True:
    
    # Find all rolls accessible in this iteration (< 4 adjacent rolls)
    # Use set comprehension for cleaner, more Pythonic code
    rolls_to_remove = {
        roll_position
        for roll_position in paper_roll_positions
        if count_adjacent_paper_rolls(roll_position, paper_roll_positions) < 4
    }
    
    # If no rolls can be removed, we're done
    if not rolls_to_remove:
        break
    
    # Remove accessible rolls using set difference (O(m) where m = rolls to remove)
    paper_roll_positions -= rolls_to_remove

# Calculate total rolls removed
final_roll_count = len(paper_roll_positions)
total_rolls_removed = initial_roll_count - final_roll_count

AoCUtils.print_solution(2, total_rolls_removed)