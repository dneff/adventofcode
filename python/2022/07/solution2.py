"""
Advent of Code 2022 - Day 7, Part 2
https://adventofcode.com/2022/day/7

This script finds the smallest directory to delete to free up enough space.
"""

import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2022/7/input')


def solve_part2():
    """
    Find the smallest directory that can be deleted to free up enough space.

    Returns:
        int: Size of the directory to delete
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

    # Calculate space requirements
    disk_total = 70000000
    disk_free_target = 30000000
    disk_used = sum(files.values())
    disk_free = disk_total - disk_used
    delete_target = disk_free_target - disk_free

    # Calculate directory sizes
    dirsizes = {}
    for d in dirs:
        size = 0
        for filepath, weight in files.items():
            if d in filepath:
                size += weight
        dirsizes[d] = size

    # Find smallest directory that meets the delete target
    target_dir = disk_total
    for v in dirsizes.values():
        if v >= delete_target:
            target_dir = min(target_dir, v)

    return target_dir


# Compute and print the answer for part 2
answer = solve_part2()
AoCUtils.print_solution(2, answer)
