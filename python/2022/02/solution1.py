"""
Advent of Code 2022 - Day 2: Rock Paper Scissors
https://adventofcode.com/2022/day/2

This script calculates the total score for a rock-paper-scissors tournament.
A/X = Rock, B/Y = Paper, C/Z = Scissors
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
    "X": "ROCK",
    "Y": "PAPER",
    "Z": "SCISSORS",
}

# Shape values
VALUES = {
    "ROCK": 1,
    "PAPER": 2,
    "SCISSORS": 3
}


def score_battle(them, us):
    """
    Calculate the score for a single round of rock-paper-scissors.

    Args:
        them: Opponent's gesture
        us: Our gesture

    Returns:
        int: Total score for the round (shape value + outcome score)
    """
    score = 0
    if us == them:
        score = 3
    elif (us == "ROCK" and them == "SCISSORS") \
            or (us == "PAPER" and them == "ROCK") \
            or (us == "SCISSORS" and them == "PAPER"):
        score = 6
    return score + VALUES[us]


def solve_part1():
    """
    Calculate the total score for all rounds of the tournament.

    Returns:
        int: Total score
    """
    lines = AoCInput.read_lines(INPUT_FILE)
    result = 0

    for line in lines:
        them, us = [GESTURES[x] for x in line.split()]
        result += score_battle(them, us)

    return result


# Compute and print the answer for part 1
answer = solve_part1()
AoCUtils.print_solution(1, answer)
