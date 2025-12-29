"""
Advent of Code 2022 - Day 1, Part 2
https://adventofcode.com/2022/day/1

This script finds the top three elves carrying the most calories and sums their totals.
"""

import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2022/1/input')


def solve_part2():
    """
    Reads the input file and finds the sum of calories carried by the top three elves.

    Returns:
        int: The sum of the top three elves' total calories.
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

    # Sort and get the top 3
    elf_calories.sort(reverse=True)

    return sum(elf_calories[:3])


# Compute and print the answer for part 2
answer = solve_part2()
AoCUtils.print_solution(2, answer)
