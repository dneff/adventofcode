"""
Advent of Code 2022 - Day 7: No Space Left On Device
https://adventofcode.com/2022/day/7

This script analyzes filesystem directory sizes and finds directories under 100000.
"""

import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2022/7/input')


def solve_part1():
    """
    Parse filesystem commands and calculate total size of directories under 100000.

    Returns:
        int: Sum of sizes of directories under 100000
    """
    lines = AoCInput.read_lines(INPUT_FILE)
    objpath = []
    files = {}
    dirs = set()

    for line in lines:
        if '$ cd ' in line:
            next_dir = line.split()[-1]
            if next_dir == '..':
                objpath.pop()
            elif next_dir == '/':
                pass
            else:
                objpath.append(next_dir)
        elif 'dir ' in line:
            dirpath = objpath[:] + [line.split()[-1]]
            dirs.add('/' + '/'.join(dirpath))
        elif line[0].isdigit():
            size, filename = line.split()
            filepath = objpath[:] + [filename]
            files['/' + '/'.join(filepath)] = int(size)

    # Calculate directory sizes
    dirsizes = {}
    for d in dirs:
        size = 0
        for filepath, weight in files.items():
            if d in filepath:
                size += weight
        dirsizes[d] = size

    # Find directories under 100000
    small_dirs = [v for v in dirsizes.values() if v <= 100000]

    return sum(small_dirs)


# Compute and print the answer for part 1
answer = solve_part1()
AoCUtils.print_solution(1, answer)
