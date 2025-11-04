"""
Advent of Code 2018 - Day 14: Chocolate Charts
https://adventofcode.com/2018/day/14

Two Elves create recipes by combining their current recipe scores. Each round:
1. They add a new recipe whose score is the sum of their current recipes
2. Each elf moves forward 1 + their current recipe score positions

Part 1: Find the scores of the ten recipes immediately after a specified number of recipes.
"""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2018/14/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def solve_part1():
    """
    Simulate recipe creation and find 10 recipes after the input number.

    Returns:
        str: Ten-digit string of recipe scores
    """
    # Read the number of recipes to skip
    num_recipes = int(AoCInput.read_lines(INPUT_FILE)[0].strip())

    # Start with initial recipes: 3 and 7
    recipes = [3, 7]
    elf1_pos = 0
    elf2_pos = 1

    # Generate recipes until we have enough
    while len(recipes) < num_recipes + 10:
        # Calculate new recipe(s) from sum of current recipes
        recipe_sum = recipes[elf1_pos] + recipes[elf2_pos]

        # Add each digit of the sum as a new recipe
        if recipe_sum >= 10:
            recipes.append(1)
            recipes.append(recipe_sum % 10)
        else:
            recipes.append(recipe_sum)

        # Move each elf forward
        elf1_pos = (elf1_pos + recipes[elf1_pos] + 1) % len(recipes)
        elf2_pos = (elf2_pos + recipes[elf2_pos] + 1) % len(recipes)

    # Extract the 10 recipes after num_recipes
    result_recipes = recipes[num_recipes:num_recipes + 10]
    return ''.join(str(score) for score in result_recipes)


# Compute and print the answer
answer = solve_part1()
AoCUtils.print_solution(1, answer)