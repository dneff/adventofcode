"""
Advent of Code 2018 - Day 14: Chocolate Charts
https://adventofcode.com/2018/day/14

Two Elves create recipes by combining their current recipe scores. Each round:
1. They add a new recipe whose score is the sum of their current recipes
2. Each elf moves forward 1 + their current recipe score positions

Part 2: Find how many recipes appear before the input sequence first appears.
"""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2018/14/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def solve_part2():
    """
    Simulate recipe creation until the input sequence appears.

    Returns:
        int: Number of recipes before the input sequence appears
    """
    # Read the target sequence
    target_sequence = AoCInput.read_lines(INPUT_FILE)[0].strip()

    # Start with initial recipes: 3 and 7
    recipes = [3, 7]
    elf1_pos = 0
    elf2_pos = 1

    # Keep track of recent recipes as a string for pattern matching
    recent_window = '37'

    # Generate recipes until target sequence appears
    while target_sequence not in recent_window:
        # Calculate new recipe(s) from sum of current recipes
        recipe_sum = recipes[elf1_pos] + recipes[elf2_pos]

        # Add each digit of the sum as a new recipe
        if recipe_sum >= 10:
            recipes.append(1)
            recipes.append(recipe_sum % 10)
            recent_window += '1' + str(recipe_sum % 10)
        else:
            recipes.append(recipe_sum)
            recent_window += str(recipe_sum)

        # Keep only last 20 characters for efficiency
        if len(recent_window) > 20:
            recent_window = recent_window[-20:]

        # Move each elf forward
        elf1_pos = (elf1_pos + recipes[elf1_pos] + 1) % len(recipes)
        elf2_pos = (elf2_pos + recipes[elf2_pos] + 1) % len(recipes)

    # Find the exact position of the sequence in all recipes
    all_recipes_str = ''.join(str(score) for score in recipes)
    return all_recipes_str.index(target_sequence)


# Compute and print the answer
answer = solve_part2()
AoCUtils.print_solution(2, answer)