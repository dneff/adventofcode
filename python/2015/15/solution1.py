import os
import sys
import math
from collections import defaultdict

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/15/input')


def isNumber(x):
    try:
        int(x)
        return True
    except ValueError:
        return False


def scoreRecipe(ingredients, measures):
    properties = ['capacity', 'durability', 'flavor', 'texture']
    property_scores = defaultdict(int)

    for idx, prop in enumerate(properties):
        for i_idx, ingredient in enumerate(ingredients):
            property_scores[prop] += measures[i_idx] * getattr(ingredient, prop)

    valid = [x for x in property_scores.values() if x > 0]
    result = math.prod(valid)
    return result


class Ingredient:
    def __init__(self, name, capacity, durability, flavor, texture, calories):
        self.name = name
        self.capacity = capacity
        self.durability = durability
        self.flavor = flavor
        self.texture = texture
        self.calories = calories


def solve_part1():
    lines = AoCInput.read_lines(INPUT_FILE)

    ingredients = []
    max_count = 100

    for line in lines:
        line = line.strip().replace(",", "").replace(":", "").split()
        name = line[0]
        capacity, durability, flavor, texture, calories = [int(x) for x in line if isNumber(x)]
        i = Ingredient(name, capacity, durability, flavor, texture, calories)
        ingredients.append(i)

    max_score = 0
    for i1 in range(1, max_count):
        for i2 in range(1, max_count - i1):
            for i3 in range(1, max_count - i1 - i2):
                i4 = max_count - i1 - i2 - i3
                weights = [i1, i2, i3, i4]
                max_score = max(max_score, scoreRecipe(ingredients, weights))

    return max_score


answer = solve_part1()
AoCUtils.print_solution(1, answer)
