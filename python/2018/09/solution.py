"""
Advent of Code 2018 - Day 9: Marble Mania
https://adventofcode.com/2018/day/9

Elves play a marble game where players take turns placing numbered marbles in a circle.
Most marbles are placed between positions 1-2 clockwise from the current marble. However,
when placing a marble whose number is divisible by 23:
- The player keeps that marble (adds to score)
- The marble 7 positions counter-clockwise is removed and added to score
- The marble immediately clockwise becomes the current marble

Part 1: Find the highest score after all marbles are placed.
Part 2: Same game but with 100x more marbles (requires efficient implementation).
"""

import os
import sys
from collections import deque, defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2018/09/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def place_marble(circle, marble_value):
    """
    Place a marble in the circle following the game rules.

    Args:
        circle: Deque representing the marble circle (current marble at left)
        marble_value: The value of the marble being placed

    Returns:
        int: Score earned from placing this marble
    """
    score = 0

    if marble_value % 23 == 0:
        # Special case: marble divisible by 23
        # Keep this marble and remove marble 7 positions counter-clockwise
        score += marble_value
        circle.rotate(7)  # Rotate to bring target marble to the left
        score += circle.popleft()  # Remove and score that marble
    else:
        # Normal case: place marble between 1-2 clockwise positions
        circle.rotate(-2)  # Rotate to position for insertion
        circle.appendleft(marble_value)  # Insert new current marble

    return score


def play_marble_game(num_players, last_marble_value):
    """
    Simulate the complete marble game.

    Args:
        num_players: Number of players in the game
        last_marble_value: Value of the last marble to be placed

    Returns:
        int: Highest score achieved by any player
    """
    circle = deque([0])  # Start with marble 0
    scores = defaultdict(int)

    # Place marbles 1 through last_marble_value
    for marble_value in range(1, last_marble_value + 1):
        player = marble_value % num_players
        scores[player] += place_marble(circle, marble_value)

    return max(scores.values())


def solve():
    """
    Parse input and solve both parts of the marble game.

    Returns:
        tuple: (part1_answer, part2_answer)
    """
    # Parse input: "463 players; last marble is worth 71787 points"
    line = AoCInput.read_lines(INPUT_FILE)[0]
    parts = line.split()
    num_players = int(parts[0])
    last_marble = int(parts[6])

    # Part 1: Original game
    part1_answer = play_marble_game(num_players, last_marble)

    # Part 2: Game with 100x more marbles
    part2_answer = play_marble_game(num_players, last_marble * 100)

    return part1_answer, part2_answer


# Compute and print both answers
part1, part2 = solve()
AoCUtils.print_solution(1, part1)
AoCUtils.print_solution(2, part2)