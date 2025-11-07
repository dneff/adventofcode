"""
Advent of Code 2017 - Day 21: Fractal Art (Part 1)

An art program generates patterns by iteratively enhancing a grid using transformation rules.
Starting with a 3x3 pattern (.#./..#/###), the process works as follows:

1. If the grid size is divisible by 2, split into 2x2 squares and enhance each to 3x3
2. If the grid size is divisible by 3, split into 3x3 squares and enhance each to 4x4
3. Join the enhanced squares back into a single larger grid
4. Repeat

Enhancement rules may require rotating or flipping patterns to find a match.

After 5 iterations, count how many pixels are "on" (#).
"""
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/21/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402
from math import isqrt  # noqa: E402


def rotate_patterns(pattern):
    """Generate all rotations and flips of a pattern.

    Args:
        pattern: A pattern string with rows separated by '/' (e.g., '../.#')

    Returns:
        A set of all unique orientations (rotations and flips) of the pattern
    """
    pattern = pattern.split('/')
    if len(pattern) == 2 and len(pattern[0]) == 2:
        pass
    elif len(pattern) == 3 and len(pattern[0]) == 3:
        pass
    else:
        raise ValueError('pattern must be only 2x2 or 3x3')
    rotations = ['/'.join(pattern)]

    # Generate 3 additional rotations (90, 180, 270 degrees)
    rotated = pattern[:]
    for _ in range(3):
        rotated = list(zip(*rotated[::-1]))
        rotated = [''.join(list(x)) for x in rotated]
        rotations.append('/'.join(rotated))

    # Flip top/bottom and add its rotations
    flip = pattern[:]
    flip[0], flip[-1] = flip[-1], flip[0]
    rotations.append('/'.join(flip))
    for _ in range(3):
        flip = list(zip(*flip[::-1]))
        flip = [''.join(list(x)) for x in flip]
        rotations.append('/'.join(flip))

    # Flip left/right and add its rotations
    flip_side = pattern[:]
    flip_side = [line[::-1] for line in flip_side]
    rotations.append('/'.join(flip_side))
    for _ in range(3):
        flip_side = list(zip(*flip_side[::-1]))
        flip_side = [''.join(list(x)) for x in flip_side]
        rotations.append('/'.join(flip_side))
    return set(rotations)


def join_patterns(pattern_list):
    """Join a list of square patterns back into a single larger pattern.

    Args:
        pattern_list: List of pattern strings to join

    Returns:
        A single pattern string representing the joined grid
    """
    if not isinstance(pattern_list, list):
        raise TypeError('join_patterns: not a list')
    length = len(pattern_list)

    if length == 1:
        return pattern_list[0]
    elif length % 2 == 0:
        pass
    elif length % 3 == 0:
        pass
    else:
        raise ValueError('join_patterns: pattern list length must be divisible by 2 or 3')

    # Arrange patterns in a square grid
    step = isqrt(length)
    final_pattern = []
    for i in range(0, length, step):
        scope = [x.split('/') for x in pattern_list[i:i + step]]
        # Concatenate corresponding rows from each pattern in this row of patterns
        for idx in range(len(scope[0])):
            full_row = ''.join([x[idx] for x in scope])
            final_pattern.append(full_row)

    return '/'.join(final_pattern)


def split_pattern(pattern):
    """Split a pattern into smaller square patterns.

    If the pattern size is divisible by 2, split into 2x2 patterns.
    If the pattern size is divisible by 3, split into 3x3 patterns.

    Args:
        pattern: A pattern string with rows separated by '/'

    Returns:
        List of smaller pattern strings
    """
    pattern = pattern.split('/')
    width, length = len(pattern), len(pattern[0])
    if width % 2 == 0 and length % 2 == 0:
        split_size = 2
    elif width % 3 == 0 and length % 3 == 0:
        split_size = 3
    else:
        raise ValueError('pattern width and length must be divisible by 2 or 3')

    separated = []
    for row in range(0, width, split_size):
        for col in range(0, length, split_size):
            small_pattern = []
            for i in range(split_size):
                small_pattern.append(pattern[row+i][col:col+split_size])
            separated.append('/'.join(small_pattern))
    return separated


def find_enhancement(enhancements, patterns):
    """Find the enhancement rule that matches one of the pattern orientations.

    Args:
        enhancements: Dictionary mapping patterns to their enhancements
        patterns: Set of all orientations of a pattern

    Returns:
        The enhanced pattern string
    """
    result = set(enhancements.keys()).intersection(set(patterns))
    if len(result) != 1:
        raise ValueError(f"find_enhancement: result not unique - {result}")
    return enhancements[result.pop()]


def main():
    """Run the fractal art program for 5 iterations and count lit pixels."""
    lines = AoCInput.read_lines(INPUT_FILE)

    # Parse enhancement rules
    enhancements = {}
    for line in lines:
        k, v = line.strip().split(' => ')
        enhancements[k] = v

    # Start with the initial pattern
    cycle_count = 5
    pattern = '.#./..#/###'
    for _ in range(cycle_count):
        new_pattern = []
        separated = split_pattern(pattern)
        for p in separated:
            new_pattern.append(find_enhancement(enhancements, rotate_patterns(p)))
        pattern = join_patterns(new_pattern)

    AoCUtils.print_solution(1, pattern.count('#'))


if __name__ == "__main__":
    main()
