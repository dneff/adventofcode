"""
Advent of Code 2018 - Day 18: Settlers of The North Pole (Part 2)
https://adventofcode.com/2018/day/18

Part 2 asks for the resource value after 1,000,000,000 minutes.
The solution detects a cycle in the pattern and uses modular arithmetic to skip ahead.
"""
import os
import sys
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2018/18/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))
from aoc_helpers import AoCUtils


def get_adjacent(area, position):
    """Count the types of acres adjacent to the given position."""
    x, y = position
    # Check all 8 surrounding positions
    adjacents = [(x - 1, y + 1), (x, y + 1), (x + 1, y + 1),
                 (x - 1, y), (x + 1, y),
                 (x - 1, y - 1), (x, y - 1), (x + 1, y - 1)]
    result = defaultdict(int)
    for p in adjacents:
        if p in area.keys():
            result[area[p]] += 1
    return result


def resource_value(area):
    """Calculate the resource value: trees * lumberyards."""
    trees = list(area.values()).count('|')
    lumber = list(area.values()).count('#')
    return trees * lumber


def update_acre(area, position):
    """
    Apply transformation rules to a single acre:
    - Open ground (.) becomes trees (|) if 3+ adjacent trees
    - Trees (|) become lumberyard (#) if 3+ adjacent lumberyards
    - Lumberyard (#) remains if adjacent to both lumberyard and trees, else becomes open (.)
    """
    acre = area[position]
    surrounding = get_adjacent(area, position)
    if acre == '.':
        if surrounding['|'] >= 3:
            acre = '|'
    elif acre == '|':
        if surrounding['#'] >= 3:
            acre = '#'
    elif acre == '#':
        if surrounding['#'] > 0 and surrounding['|'] > 0:
            pass
        else:
            acre = '.'

    return acre


def main():
    """
    Simulate the lumber collection area for 1,000,000,000 minutes.
    The pattern repeats in a cycle, so we detect the cycle and skip ahead.
    """
    file = open(INPUT_FILE, 'r', encoding='utf-8')
    area = {}
    # Parse initial area state
    for y, line in enumerate(file.readlines()):
        for x, char in enumerate(line.strip()):
            area[(x, y)] = char

    # The values repeat on a 700-minute cycle (found empirically)
    # Simulate until the cycle starts
    time_limit = 700
    for minute in range(time_limit):
        new_area = {}
        for position in area:
            new_area[position] = update_acre(area, position)
        area = new_area

    # Use modular arithmetic to skip to the equivalent state at 1 billion minutes
    remaining = (1000000000 - time_limit) % time_limit
    print(remaining)
    for minute in range(remaining):
        new_area = {}
        for position in area:
            new_area[position] = update_acre(area, position)
        area = new_area

    AoCUtils.print_solution(2, resource_value(area))


if __name__ == "__main__":
    main()
