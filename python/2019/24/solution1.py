"""
Advent of Code 2019 - Day 24: Planet of Discord
https://adventofcode.com/2019/day/24


Eris isn't a very large place; a scan of the entire area fits into a 5x5 grid 
(your puzzle input). The scan shows bugs (#) and empty spaces (.).

Each minute, The bugs live and die based on the number of bugs in the four 
adjacent tiles:

A bug dies (becoming an empty space) unless there is exactly one bug adjacent to it.
An empty space becomes infested with a bug if exactly one or two bugs are adjacent to it.
Otherwise, a bug or empty space remains the same.

Part 1

To calculate the biodiversity rating for this layout, consider each tile left-to-right 
in the top row, then left-to-right in the second row, and so on. Each of these tiles is 
worth biodiversity points equal to increasing powers of two: 1, 2, 4, 8, 16, 32, and so 
on. Add up the biodiversity points for tiles with bugs; in this example, the 16th tile 
(32768 points) and 22nd tile (2097152 points) have bugs, a total biodiversity 
rating of 2129920.

What is the biodiversity rating for the first layout that appears twice?

STRATEGY:
convert the tiles to a list of integers, where each integer represents a tile. This should
make it easier to calculate the biodiversity rating.

"""

import os
import sys


# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "../../"))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, "../../../../aoc-data/2019/24/input")

tiles = ''.join(AoCInput.read_lines(INPUT_FILE))

# convert tiles to a list of integers, where each integer represents a tile. This should 
# make it easier to calculate the biodiversity rating.
tiles = [1 if tile == '#' else 0 for tile in tiles]

# create dictionary of adjacent tiles. account for the fact this is a list of integers 
# representing a 5x5 grid.
# for a given index i, the adjacent tiles are at indices i-5, i+5, i-1, and i+1, but only 
# if those indices are within the bounds of the grid.

adjacent_tiles = {}
for i in range(25):
    adjacent_tiles[i] = []
    if i - 5 >= 0:
        adjacent_tiles[i].append(i - 5)
    if i + 5 < 25:
        adjacent_tiles[i].append(i + 5)
    if i % 5 != 0:
        adjacent_tiles[i].append(i - 1)
    if (i + 1) % 5 != 0:
        adjacent_tiles[i].append(i + 1)


def calculate_biodiversity_rating(tiles):
    """
    each index is twice the value of the previous one, starting with 1 for the first tile.
    """
    biodiversity_rating = 0
    for i, tile in enumerate(tiles):
        if tile == 1:
            biodiversity_rating += 2 ** i
    return biodiversity_rating

def simulate_minute(tiles, adjacent_tiles):
    """
    Simulate one minute of the bug life cycle.
    """
    new_tiles = tiles.copy()
    for i, tile in enumerate(tiles):
        adjacent_bugs = sum(tiles[j] for j in adjacent_tiles[i])
        # A bug dies (becoming an empty space) unless there is exactly one bug adjacent to it.
        if tile == 1 and adjacent_bugs != 1:
            new_tiles[i] = 0
        # An empty space becomes infested with a bug if exactly one or two bugs are adjacent to it.
        # Otherwise, a bug or empty space remains the same.
        elif tile == 0 and (adjacent_bugs == 1 or adjacent_bugs == 2):
            new_tiles[i] = 1
    return new_tiles


# simulate the bug life cycle until a layout appears twice.
previous_ratings = set()
current_rating = calculate_biodiversity_rating(tiles)
while current_rating not in previous_ratings:
    previous_ratings.add(current_rating)
    tiles = simulate_minute(tiles, adjacent_tiles)
    current_rating = calculate_biodiversity_rating(tiles)

AoCUtils.print_solution(1, current_rating)
