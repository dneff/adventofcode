"""
Advent of Code 2018 - Day 12: Subterranean Sustainability
https://adventofcode.com/2018/day/12

Simulate plant growth across numbered pots using a set of rules.
Each rule determines whether a pot will contain a plant based on its current state
and the state of its two neighbors on each side.

Part 2: After 50 billion generations, calculate the sum of pot numbers containing plants.
The pattern stabilizes after some generations, growing linearly, so we can extrapolate.
"""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2018/12/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def process_generation(rules, pots):
    """
    Apply growth rules to generate the next generation of pots.

    Args:
        rules: Dictionary mapping 5-character patterns to outcomes ('#' or '.')
        pots: String representing current pot states

    Returns:
        str: New generation of pot states
    """
    new_pots = ['.'] * len(pots)

    for idx in range(len(pots)):
        pattern = ''.join(pots[idx - 2:idx + 3])
        if pattern in rules:
            new_pots[idx] = rules[pattern]

    return ''.join(new_pots)


def score_pots(pots, offset):
    """
    Calculate the sum of pot numbers containing plants.

    Args:
        pots: String representing pot states
        offset: Number of padding positions added to the left

    Returns:
        int: Sum of pot numbers (adjusted for offset) containing plants
    """
    total = 0
    for idx in range(len(pots)):
        if pots[idx] == '#':
            total += idx - offset

    return total


def solve_part2():
    """
    Simulate plant growth for 50 billion generations using pattern detection.

    The pattern eventually stabilizes and grows linearly. We detect this by
    simulating until the score difference becomes constant, then extrapolate.

    Returns:
        int: Sum of pot numbers containing plants after 50 billion generations
    """
    lines = AoCInput.read_lines(INPUT_FILE)

    # Parse initial state
    initial_state = lines[0].split(': ')[1]

    # Add plenty of padding for 50 billion generations
    offset = 2000
    padding = '.' * offset
    pots = padding + initial_state + padding

    # Parse rules
    rules = {}
    for line in lines[2:]:
        pattern, outcome = line.split(' => ')
        rules[pattern] = outcome

    # Simulate until pattern stabilizes (score increases by constant amount)
    target_generations = 50_000_000_000
    stabilization_check = 200  # Generations to simulate before checking for stability

    score_history = []
    for generation in range(stabilization_check):
        pots = process_generation(rules, pots)
        score_history.append(score_pots(pots, offset))

    # After stabilization, the score increases by a constant amount each generation
    score_delta = score_history[-1] - score_history[-2]
    remaining_generations = target_generations - stabilization_check

    # Extrapolate the final score
    final_score = score_history[-1] + (remaining_generations * score_delta)

    return final_score


# Compute and print the answer
answer = solve_part2()
AoCUtils.print_solution(2, answer)