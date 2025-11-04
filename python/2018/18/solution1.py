"""
Advent of Code 2018 - Day 18: Settlers of The North Pole (Part 1)
https://adventofcode.com/2018/day/18

On the outskirts of the North Pole base construction project, many Elves are collecting lumber.
The lumber collection area is 50 acres by 50 acres; each acre can be either open ground (.),
trees (|), or a lumberyard (#). This solution simulates the area changes over time.
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
    """Simulate the lumber collection area for 10 minutes."""
    file = open(INPUT_FILE, 'r', encoding='utf-8')
    area = {}
    # Parse initial area state
    for y, line in enumerate(file.readlines()):
        for x, char in enumerate(line.strip()):
            area[(x, y)] = char

    # Simulate 10 minutes of changes
    time_limit = 10
    for minute in range(time_limit):
        new_area = {}
        for position in area:
            new_area[position] = update_acre(area, position)
        area = new_area

    AoCUtils.print_solution(1, resource_value(area))


if __name__ == "__main__":
    main()
