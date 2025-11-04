"""
Advent of Code 2018 - Day 1: Chronal Calibration (Part 2)
https://adventofcode.com/2018/day/1

Find the first frequency reached twice while repeatedly cycling through the sequence
of frequency changes. The device repeats its list of frequency changes indefinitely.

Starting at frequency 0, the device applies changes until it reaches a frequency it
has seen before, then reports that frequency.
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2018/1/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def solve_part2():
    """
    Find the first frequency that is reached twice while cycling through changes.

    Returns:
        int: The first frequency reached twice
    """
    frequency_changes = [int(line.strip()) for line in AoCInput.read_lines(INPUT_FILE)]
    current_frequency = 0
    seen_frequencies = {0}  # Start by tracking the initial frequency

    # Keep cycling through the frequency changes until we find a duplicate
    while True:
        for change in frequency_changes:
            current_frequency += change

            if current_frequency in seen_frequencies:
                return current_frequency

            seen_frequencies.add(current_frequency)


# Compute and print the answer for part 2
first_duplicate_frequency = solve_part2()
AoCUtils.print_solution(2, first_duplicate_frequency)
