import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/19/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils

def traverse_circle(starting_elf, elf_circle, num_steps):
    """
    Traverse the circular linked list of elves.

    Args:
        starting_elf: The elf ID to start from
        elf_circle: Dictionary representing circular linked list (elf_id -> next_elf_id)
        num_steps: Number of steps to traverse around the circle

    Returns:
        The elf ID after traversing num_steps positions
    """
    current_position = starting_elf
    while num_steps > 0:
        current_position = elf_circle[current_position]
        num_steps -= 1

    return current_position


def main():
    # Day 19 Part 2: An Elephant Named Joseph
    # New rules: Elves steal from the elf directly ACROSS the circle (instead of to the left)
    # If two elves are across, steal from the one on the left (from stealer's perspective)
    # Elves with no presents are removed from the circle
    # Test case: With 5 elves, Elf 2 gets all the presents

    # Puzzle input: Number of elves in the circle
    # num_elves = 5  # Test case: Should output 2
    num_elves = 3004953

    # Build a circular linked list where each elf points to the next elf in the circle
    # Key: current elf ID, Value: next elf ID in the circle
    elf_circle = {}
    for elf_id in range(1, num_elves):
        elf_circle[elf_id] = elf_id + 1
    elf_circle[num_elves] = 1  # Last elf points back to first elf (circular)

    # Start with Elf 1 taking the first turn
    current_elf = 1

    # Track how many elves remain in the circle
    elves_remaining = num_elves

    # Find the elf directly across the circle from current_elf
    # For a circle of size N, the opposite elf is N//2 steps away
    # We traverse N//2 - 1 steps because we're already at position 0
    offset_to_opposite = elves_remaining // 2 - 1
    opposite_elf = traverse_circle(current_elf, elf_circle, offset_to_opposite)

    # Continue until only 2 elves remain (edge case handled separately)
    while elves_remaining > 2:
        # Update opposite_elf pointer for the next round
        # If even number of elves, the opposite shifts by 1 after removal
        if elves_remaining % 2 == 0:
            opposite_elf = elf_circle[opposite_elf]

        # Remove the opposite elf from the circle by updating the linked list
        # Point the elf before opposite_elf to the elf after opposite_elf
        elf_circle[opposite_elf] = elf_circle[elf_circle[opposite_elf]]

        # One elf has been eliminated
        elves_remaining -= 1

        # Move to the next elf's turn
        current_elf = elf_circle[current_elf]

    # The last remaining elf is the winner who gets all the presents
    AoCUtils.print_solution(2, current_elf)
    
    

if __name__ == "__main__":
    main()