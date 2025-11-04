"""
Advent of Code 2018 - Day 12: Subterranean Sustainability
https://adventofcode.com/2018/day/12

Simulate plant growth across numbered pots over 20 generations using a set of rules.
Each rule determines whether a pot will contain a plant based on its current state
and the state of its two neighbors on each side.

Part 1: After 20 generations, calculate the sum of all pot numbers containing plants.
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

    Each pot's next state is determined by examining a 5-pot window
    (itself and 2 neighbors on each side) and matching against rules.

    Args:
        rules: Dictionary mapping 5-character patterns to outcomes ('#' or '.')
        pots: String representing current pot states

    Returns:
        str: New generation of pot states
    """
    new_pots = ['.'] * len(pots)

    for idx in range(len(pots)):
        # Get 5-pot window (current pot and 2 neighbors on each side)
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
            # Adjust index by offset to get actual pot number
            total += idx - offset

    return total


def solve_part1():
    """
    Simulate 20 generations and calculate the sum of pot numbers with plants.

    Returns:
        int: Sum of pot numbers containing plants after 20 generations
    """
    lines = AoCInput.read_lines(INPUT_FILE)

    # Parse initial state: "initial state: #..#.#..##......###...###"
    initial_state = lines[0].split(': ')[1]

    # Add padding to allow plants to spread
    offset = 50
    padding = '.' * offset
    pots = padding + initial_state + padding

    # Parse rules (skip blank line at index 1)
    rules = {}
    for line in lines[2:]:
        pattern, outcome = line.split(' => ')
        rules[pattern] = outcome

    # Simulate 20 generations
    for generation in range(20):
        pots = process_generation(rules, pots)

    return score_pots(pots, offset)


# Compute and print the answer
answer = solve_part1()
AoCUtils.print_solution(1, answer)