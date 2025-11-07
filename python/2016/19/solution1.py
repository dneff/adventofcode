import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/19/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402
AoCInput  # noqa: F401


def main():
    # Day 19: An Elephant Named Joseph
    # Problem: Elves sit in a circle and take turns stealing presents from the elf to their left.
    # An elf with no presents is removed from the circle.
    # Which elf ends up with all the presents?
    # Test case: With 5 elves, Elf 3 gets all the presents

    # Puzzle input: Number of elves in the circle
    num_elves = 3004953

    # Create list of elves (numbered 1 to num_elves) still in the circle
    elves_in_circle = list(range(1, num_elves + 1))

    # Simulate the gift-stealing game until only one elf remains
    while len(elves_in_circle) != 1:
        # Check if there's an odd number of elves in the current round
        # If odd, the last elf will steal from the first elf (wrapping around the circle)
        has_odd_count = len(elves_in_circle) % 2 == 1

        # Keep every other elf (the ones who just stole presents and survive this round)
        # elves_in_circle[::2] selects elves at positions 0, 2, 4, ... (every 2nd elf)
        elves_in_circle = elves_in_circle[::2]

        # If we had an odd count, the last elf stole from the first elf (wrapping around),
        # so the first elf in our new list should be removed in the next round
        if has_odd_count:
            elves_in_circle.pop(0)

    # The remaining elf is the winner who gets all the presents
    AoCUtils.print_solution(1, elves_in_circle[0])


if __name__ == "__main__":
    main()
