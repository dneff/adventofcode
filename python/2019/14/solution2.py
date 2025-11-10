"""
Advent of Code 2019 - Day 14: Space Stoichiometry - Part 2

Given 1 trillion ORE, determine the maximum amount of FUEL that can be produced.
Use binary search / iterative approach to find the maximum FUEL quantity.
"""
import os
import sys
import math

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/14/input')


def calculate_ore_needed(materials, reactions, distance_map, fuel_quantity):
    """
    Calculate ORE needed to produce the specified amount of FUEL.

    Args:
        materials: Set of all materials
        reactions: Dict mapping material -> {qty, ingredients}
        distance_map: Dict mapping material -> distance from ORE
        fuel_quantity: Amount of FUEL to produce

    Returns:
        Amount of ORE required
    """
    needed_materials = {'FUEL': fuel_quantity}

    while len(needed_materials) > 1 or 'ORE' not in needed_materials:
        # Process materials farthest from ORE first
        material = max(needed_materials, key=lambda x: distance_map[x])
        quantity_needed = needed_materials[material]
        del needed_materials[material]

        # Get reaction for this material
        base_quantity, ingredients = reactions[material].values()

        # Calculate how many times we need to run this reaction
        reaction_multiplier = math.ceil(quantity_needed / base_quantity)

        # Add required ingredients
        for ingredient, amount_per_reaction in ingredients.items():
            if ingredient not in needed_materials:
                needed_materials[ingredient] = 0
            needed_materials[ingredient] += reaction_multiplier * amount_per_reaction

    return needed_materials['ORE']


def parse_reactions(lines):
    """
    Parse reaction formulas into data structures.

    Returns:
        Tuple of (reactions dict, materials set, distance map)
    """
    reactions = {}
    materials = {'ORE'}
    distance = {'ORE': 0}

    # Parse all reactions
    for line in lines:
        left, right = line.strip().split(' => ')
        output_parts = right.split()
        output_material = output_parts[1]
        output_quantity = int(output_parts[0])

        # Parse ingredients
        ingredients = {}
        for ingredient_str in left.split(', '):
            parts = ingredient_str.split()
            ingredients[parts[1]] = int(parts[0])

        reactions[output_material] = {
            'qty': output_quantity,
            'ingredients': ingredients
        }
        materials.add(output_material)

    # Calculate distance from ORE for topological ordering
    while len(distance) < len(materials):
        for material in materials:
            if material in distance:
                continue
            # Check if all ingredients have been processed
            if not all(ing in distance for ing in reactions[material]['ingredients'].keys()):
                continue
            # Distance is max distance of ingredients + 1
            distance[material] = max(distance[ing] for ing in reactions[material]['ingredients'].keys()) + 1

    return reactions, materials, distance


def solve_part2():
    """Find maximum FUEL producible with 1 trillion ORE."""
    lines = AoCInput.read_lines(INPUT_FILE)
    reactions, materials, distance = parse_reactions(lines)

    total_ore_available = 1000000000000
    ore_per_fuel = calculate_ore_needed(materials, reactions, distance, 1)

    # Start with initial estimate
    fuel_target = total_ore_available // ore_per_fuel
    ore_used = calculate_ore_needed(materials, reactions, distance, fuel_target)

    # Iteratively increase until we exceed capacity
    while True:
        # Estimate how much more fuel we can make
        fuel_target += (total_ore_available - ore_used) // ore_per_fuel + 1
        ore_used = calculate_ore_needed(materials, reactions, distance, fuel_target)

        if ore_used > total_ore_available:
            break

    # We went over, so the answer is one less
    return fuel_target - 1


answer = solve_part2()
AoCUtils.print_solution(2, answer)
