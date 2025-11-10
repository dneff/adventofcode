"""
Advent of Code 2019 - Day 13: Care Package - Part 1

Run an arcade cabinet Intcode program that draws tiles to a screen. The program
outputs triplets (x, y, tile_id) where tile_id represents: 0=empty, 1=wall,
2=block, 3=paddle, 4=ball. Count how many block tiles (id=2) appear on screen
when the program exits.
"""
import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402
from IntCode import IntCode, OutputInterrupt  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/13/input')


def solve_part1():
    """Run the arcade game and count block tiles on screen."""
    program = AoCInput.read_file(INPUT_FILE).strip()

    arcade_computer = IntCode(program)
    screen_tiles = {}

    while not arcade_computer.complete:
        try:
            arcade_computer.run()
        except OutputInterrupt:
            # Collect output triplet (x, y, tile_id)
            if len(arcade_computer.output) == 3:
                x, y, tile_id = arcade_computer.output
                screen_tiles[(x, y)] = tile_id
                arcade_computer.output.clear()

    # Count block tiles (tile_id = 2)
    block_count = sum(1 for tile_id in screen_tiles.values() if tile_id == 2)
    return block_count


answer = solve_part1()
AoCUtils.print_solution(1, answer)
