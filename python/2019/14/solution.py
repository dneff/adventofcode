import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/14/input')

# very challenging to reason through
# solution from github: jcisio/adventofcode2019

import math  # noqa: E402


def oreNeeded(materials, reactions, distance, fuel):
    needed = {'FUEL': fuel}
    while len(needed) > 1 or 'ORE' not in needed:
        material = max(needed, key=lambda x: distance[x])
        quantity = needed[material]
        del needed[material]
        base_quantity, ingredients = reactions[material].values()
        for a, b in ingredients.items():
            if a not in needed:
                needed[a] = 0
            needed[a] += math.ceil(quantity/base_quantity) * b
    return needed['ORE']


def solve_part1():
    reactions = {}
    materials = {'ORE'}
    distance = {'ORE': 0}

    lines = AoCInput.read_lines(INPUT_FILE)
    for data in lines:
        l, r = data.strip().split(' => ')
        output = r.split()
        reactions[output[1]] = {
            'qty': int(output[0]),
            'ingredients': {i[1]: int(i[0]) for i in [i.split() for i in l.split(', ')]}
        }
        materials.add(output[1])

    while len(distance) < len(materials):
        for material in materials:
            if material in distance:
                continue
            if not all([i in distance for i in reactions[material]['ingredients'].keys()]):
                continue
            distance[material] = max([distance[i] for i in reactions[material]['ingredients'].keys()]) + 1

    sol1 = oreNeeded(materials, reactions, distance, 1)
    return sol1, materials, reactions, distance


def solve_part2(sol1, materials, reactions, distance):
    capacity = 1000000000000

    target = capacity//sol1
    used_ore = oreNeeded(materials, reactions, distance, target)
    while True:
        target += (capacity - used_ore)//sol1 + 1
        used_ore = oreNeeded(materials, reactions, distance, target)
        if used_ore > capacity:
            break

    return target - 1


answer1, materials, reactions, distance = solve_part1()
AoCUtils.print_solution(1, f"One fuel requires {answer1} ore")

answer2 = solve_part2(answer1, materials, reactions, distance)
AoCUtils.print_solution(2, f"Given 1 trillion ore, the maximum amount of fuel produced is {answer2}")
