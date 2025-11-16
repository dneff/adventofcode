"""
Advent of Code 2019 - Day 22: Slam Shuffle

Part 1: Determine the position of card 2019 after shuffling a deck of 10,007 cards.

The problem involves three card shuffling techniques:
1. Deal into new stack: Reverses the entire deck
2. Cut N cards: Moves the top (or bottom if N < 0) N cards to the other end
3. Deal with increment N: Distributes cards at evenly-spaced positions

Instead of simulating the entire deck, we track only the position of card 2019
by applying the mathematical transformation for each shuffle operation.
"""

import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "../../"))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, "../../../../aoc-data/2019/22/input")


def parse_instructions(lines):
    """
    Parse shuffle instructions from input lines into structured tuples.

    Args:
        lines: List of instruction strings from the puzzle input

    Returns:
        List of tuples in the format (operation_type, parameter):
        - ("new_stack", None) for reversing the deck
        - ("cut", n) for cutting n cards from top (or -n from bottom)
        - ("deal_increment", n) for dealing with increment n
    """
    instructions = []
    for line in lines:
        line = line.strip()
        if line == "deal into new stack":
            instructions.append(("new_stack", None))
        elif line.startswith("cut"):
            n = int(line.split(" ")[-1])
            instructions.append(("cut", n))
        elif line.startswith("deal with increment"):
            n = int(line.split(" ")[-1])
            instructions.append(("deal_increment", n))
    return instructions


def new_stack(position, deck_size):
    """
    Apply "deal into new stack" transformation to a card position.

    This operation reverses the entire deck. A card at position i
    moves to position (deck_size - 1 - i). For example, in a 10-card deck:
    - Position 0 -> Position 9
    - Position 1 -> Position 8
    - Position 9 -> Position 0

    Args:
        position: Current position of the card (0-indexed)
        deck_size: Total number of cards in the deck

    Returns:
        New position of the card after reversing the deck
    """
    return deck_size - 1 - position


def cut(position, n, deck_size):
    """
    Apply "cut N cards" transformation to a card position.

    This operation takes the top N cards and moves them to the bottom
    of the deck (or bottom N cards to top if N is negative). All positions
    shift by -N (modulo deck_size). For example, with N=3 in a 10-card deck:
    - Position 0 -> Position 7 (0 - 3 = -3, -3 mod 10 = 7)
    - Position 3 -> Position 0
    - Position 9 -> Position 6

    Args:
        position: Current position of the card (0-indexed)
        n: Number of cards to cut (positive = from top, negative = from bottom)
        deck_size: Total number of cards in the deck

    Returns:
        New position of the card after cutting
    """
    return (position - n) % deck_size


def deal_with_increment(position, n, deck_size):
    """
    Apply "deal with increment N" transformation to a card position.

    This operation distributes cards at evenly-spaced positions. The card
    at position i moves to position (i * n) mod deck_size. For example,
    with increment 3 in a 10-card deck:
    - Position 0 -> Position 0 (0 * 3 = 0)
    - Position 1 -> Position 3 (1 * 3 = 3)
    - Position 2 -> Position 6 (2 * 3 = 6)
    - Position 3 -> Position 9 (3 * 3 = 9)
    - Position 4 -> Position 2 (4 * 3 = 12, 12 mod 10 = 2)

    Args:
        position: Current position of the card (0-indexed)
        n: Increment value (number of positions to skip for each card)
        deck_size: Total number of cards in the deck

    Returns:
        New position of the card after dealing with increment
    """
    return (position * n) % deck_size


if __name__ == "__main__":
    # Read and parse shuffle instructions
    lines = AoCInput.read_lines(INPUT_FILE)
    instructions = parse_instructions(lines)

    # Constants from the problem
    deck_size = 10007
    target_card = 2019

    # Track the position of card 2019 through all shuffle operations
    # We apply each transformation to the position rather than simulating the entire deck
    card_position = target_card
    for instruction_type, parameter in instructions:
        if instruction_type == "new_stack":
            card_position = new_stack(card_position, deck_size)
        elif instruction_type == "cut":
            card_position = cut(card_position, parameter, deck_size)
        elif instruction_type == "deal_increment":
            card_position = deal_with_increment(card_position, parameter, deck_size)

    # Output the final position of card 2019
    AoCUtils.print_solution(1, card_position)
