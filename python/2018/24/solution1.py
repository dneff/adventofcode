"""
Advent of Code 2018 - Day 24: Immune System Simulator 20XX (Part 1)
https://adventofcode.com/2018/day/24

The immune system and the infection each have an army made up of 
several groups; each group consists of one or more identical units. 
The armies repeatedly fight until only one army has units remaining.

How many units would the winning army have?

"""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, "../../../../aoc-data/2018/24/input")
sys.path.append(os.path.join(SCRIPT_DIR, "../../"))

from aoc_helpers import AoCInput, AoCUtils, MathUtils

class Group():
    def __init__(self, units, hit_points, attack_damage, attack_type, initiative, weaknesses, immunities):
        self.units = units
        self.hit_points = hit_points
        self.attack_damage = attack_damage
        self.attack_type = attack_type
        self.initiative = initiative
        self.weaknesses = weaknesses
        self.immunities = immunities

    def effective_power(self):
        return self.units * self.attack_damage

    def damage_to(self, other):
        if self.attack_type in other.immunities:
            return 0
        damage = self.effective_power()
        if self.attack_type in other.weaknesses:
            damage *= 2
        return damage
    
    __repr__ = lambda self: f"Group(units={self.units}, hp={self.hit_points}, atk={self.attack_damage} type={self.attack_type}, init={self.initiative}, weak={self.weaknesses}, immune={self.immunities})"

def create_group(input_line):
    """ 
    Create a Group object from an input line describing the group.
    Args:
        input_line (str): The input line describing the group
    Returns:
        Group: The created Group object

    example input: 1994 units each with 48414 hit points (immune to slashing) with an attack that does 46 cold damage at initiative 3
    """
    parts = input_line.split(" ")
    units = int(parts[0])
    hit_points = int(parts[4])
    initiative = int(parts[-1])
    attack_damage = int(parts[-6])
    attack_type = parts[-5]

    weaknesses = []
    immunities = []
    if "(" in input_line:
        attributes = input_line[input_line.find("(")+1:input_line.find(")")].split("; ")
        for attribute in attributes:
            if attribute.startswith("weak to "):
                weaknesses = attribute[len("weak to "):].split(", ")
            elif attribute.startswith("immune to "):
                immunities = attribute[len("immune to "):].split(", ")

    group = Group(units, hit_points, attack_damage, attack_type, initiative, weaknesses, immunities)
    return group

instructions = [line.strip() for line in AoCInput.read_lines(INPUT_FILE)]
for idx, line in enumerate(instructions):
    if line == "":
        separator_index = idx
        print(f"separator_index = {separator_index}")
    print(f"instructions[{idx}] = {line}")

immune = []
immune_instructions = instructions[1:separator_index]
for line in immune_instructions:
    immune.append(create_group(line))

infection = []
infection_instructions = instructions[separator_index+2:]
for line in infection_instructions:
    infection.append(create_group(line))

print("Immune System Groups:")
for group in immune:
    print(group)

print("\nInfection Groups:")
for group in infection:
    print(group)


while len(immune) > 0 and len(infection) > 0:
    # Target Selection Phase
    all_groups = immune + infection
    all_groups.sort(key=lambda g: (g.effective_power(), g.initiative), reverse=True)

    targets = {}
    targeted = set()

    for group in all_groups:
        if group in immune:
            enemies = infection
        else:
            enemies = immune

        best_target = None
        max_damage = 0
        for enemy in enemies:
            if enemy in targeted:
                continue
            damage = group.damage_to(enemy)
            if damage > max_damage or (damage == max_damage and (enemy.effective_power(), enemy.initiative) > (best_target.effective_power(), best_target.initiative) if best_target else (0,0)):
                max_damage = damage
                best_target = enemy

        if best_target and max_damage > 0:
            targets[group] = best_target
            targeted.add(best_target)

    # Attacking Phase
    all_groups.sort(key=lambda g: g.initiative, reverse=True)

    for group in all_groups:
        if group.units <= 0:
            continue
        if group not in targets:
            continue

        target = targets[group]
        damage = group.damage_to(target)
        units_lost = damage // target.hit_points
        target.units -= units_lost
        if target.units < 0:
            target.units = 0

    # Remove dead groups
    immune = [g for g in immune if g.units > 0]
    infection = [g for g in infection if g.units > 0]

# Calculate remaining units
remaining_units = sum(g.units for g in immune + infection)
AoCUtils.print_solution(1, remaining_units)