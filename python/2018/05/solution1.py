"""
Advent of Code 2018 - Day 5: Alchemical Reduction (Part 1)
https://adventofcode.com/2018/day/5

Process a polymer composed of units (letters). Units of the same type but opposite
polarity (uppercase/lowercase) react and destroy each other.

Reaction Rules:
- Same type, opposite polarity (e.g., 'r' and 'R') → react and disappear
- Same type, same polarity (e.g., 'r' and 'r') → no reaction
- Different types (e.g., 'r' and 's') → no reaction

Example: dabAcCaCBAcCcaDA reduces to dabCBAcaDA (10 units)

Question: How many units remain after fully reacting the polymer?
"""

import os
import sys
from collections import deque
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2018/5/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def units_react(unit1, unit2):
    """
    Check if two polymer units will react (same type, opposite polarity).

    Args:
        unit1: First unit (character)
        unit2: Second unit (character)

    Returns:
        bool: True if units react and destroy each other
    """
    # Must be same type (letter) but different case (polarity)
    return (unit1.lower() == unit2.lower() and
            ((unit1.islower() and unit2.isupper()) or
             (unit1.isupper() and unit2.islower())))


def react_polymer(polymer):
    """
    Fully react a polymer by removing adjacent units that react.

    Args:
        polymer: String representing the polymer

    Returns:
        int: Number of units remaining after all reactions
    """
    reacted_polymer = deque()

    for unit in polymer:
        # If polymer is empty, add the unit
        if len(reacted_polymer) == 0:
            reacted_polymer.appendleft(unit)
            continue

        # Check if current unit reacts with the last unit in the polymer
        if units_react(unit, reacted_polymer[0]):
            # They react - remove the last unit (current unit is destroyed too)
            reacted_polymer.popleft()
        else:
            # No reaction - add the current unit
            reacted_polymer.appendleft(unit)

    return len(reacted_polymer)


def solve_part1():
    """
    React the polymer and count remaining units.

    Returns:
        int: Number of units remaining after full reaction
    """
    polymer = AoCInput.read_lines(INPUT_FILE)[0].strip()
    return react_polymer(polymer)


# Compute and print the answer for part 1
remaining_units = solve_part1()
AoCUtils.print_solution(1, remaining_units)
