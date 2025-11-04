"""
Advent of Code 2018 - Day 5: Alchemical Reduction (Part 2)
https://adventofcode.com/2018/day/5

Improve the polymer by removing all units of one type (both polarities) before
reacting. Find which unit type to remove to produce the shortest polymer.

Strategy: Try removing each unit type (A/a, B/b, C/c, etc.), react the remaining
polymer, and find which produces the shortest result.
"""

import os
import sys
from collections import deque
from string import ascii_uppercase
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
    return (unit1.lower() == unit2.lower() and
            ((unit1.islower() and unit2.isupper()) or
             (unit1.isupper() and unit2.islower())))


def react_polymer(polymer, skip_unit=None):
    """
    React a polymer, optionally skipping all instances of a specific unit type.

    Args:
        polymer: String representing the polymer
        skip_unit: Unit type to skip (both polarities), or None

    Returns:
        int: Number of units remaining after all reactions
    """
    reacted_polymer = deque()

    for unit in polymer:
        # Skip this unit type if specified
        if skip_unit and unit.upper() == skip_unit.upper():
            continue

        # If polymer is empty, add the unit
        if len(reacted_polymer) == 0:
            reacted_polymer.appendleft(unit)
            continue

        # Check if current unit reacts with the last unit in the polymer
        if units_react(unit, reacted_polymer[0]):
            # They react - remove the last unit
            reacted_polymer.popleft()
        else:
            # No reaction - add the current unit
            reacted_polymer.appendleft(unit)

    return len(reacted_polymer)


def solve_part2():
    """
    Find the shortest polymer by removing one unit type before reacting.

    Returns:
        int: Length of shortest polymer after optimal unit type removal
    """
    polymer = AoCInput.read_lines(INPUT_FILE)[0].strip()

    # Try removing each unit type and track the resulting polymer lengths
    shortest_length = float('inf')

    for unit_type in ascii_uppercase:
        # React polymer with this unit type removed
        length = react_polymer(polymer, skip_unit=unit_type)
        shortest_length = min(shortest_length, length)

    return shortest_length


# Compute and print the answer for part 2
shortest_polymer_length = solve_part2()
AoCUtils.print_solution(2, shortest_polymer_length)
