"""
Advent of Code 2022 - Day 1: Calorie Counting
https://adventofcode.com/2022/day/1

This script finds the elf carrying the most calories.
Each elf's inventory is separated by blank lines in the input.
"""

import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2022/1/input')


def solve_part1():
    """
    Reads the input file and finds the maximum total calories carried by any elf.

    Returns:
        int: The maximum total calories carried by a single elf.
    """
    lines = AoCInput.read_lines(INPUT_FILE)

    elf_calories = []
    current_elf = 0

    for line in lines:
        if line == '':
            elf_calories.append(current_elf)
            current_elf = 0
        else:
            current_elf += int(line)

    # Don't forget the last elf
    elf_calories.append(current_elf)

    return max(elf_calories)


# Compute and print the answer for part 1
answer = solve_part1()
AoCUtils.print_solution(1, answer)
