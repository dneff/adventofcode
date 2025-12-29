"""
Advent of Code 2022 - Day 2, Part 2
https://adventofcode.com/2022/day/2

This script calculates the total score when X/Y/Z represent desired outcomes.
X = lose, Y = draw, Z = win
"""

import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2022/2/input')

# Gesture mappings
GESTURES = {
    "A": "ROCK",
    "B": "PAPER",
    "C": "SCISSORS",
}

# Shape values
VALUES = {
    "ROCK": 1,
    "PAPER": 2,
    "SCISSORS": 3
}


def score_battle(them, outcome):
    """
    Calculate the score based on opponent's gesture and desired outcome.

    Args:
        them: Opponent's gesture code (A/B/C)
        outcome: Desired outcome code (X/Y/Z)

    Returns:
        int: Total score for the round
    """
    them_value = VALUES[GESTURES[them]]

    if outcome == "X":  # Need to lose
        score = them_value - 1
        if score == 0:
            score = 3
        return score
    elif outcome == "Y":  # Need to draw
        return 3 + them_value
    elif outcome == "Z":  # Need to win
        score = them_value + 1
        if score == 4:
            score = 1
        return 6 + score


def solve_part2():
    """
    Calculate the total score for all rounds based on desired outcomes.

    Returns:
        int: Total score
    """
    lines = AoCInput.read_lines(INPUT_FILE)
    result = 0

    for line in lines:
        them, outcome = line.split()
        result += score_battle(them, outcome)

    return result


# Compute and print the answer for part 2
answer = solve_part2()
AoCUtils.print_solution(2, answer)
