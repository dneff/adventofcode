import os
import sys
import re
from collections import defaultdict

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/19/input')


def solve_part1():
    """
    Solve Day 19 Part 1: Medicine for Rudolph

    Count how many distinct molecules can be created by doing exactly one
    replacement on the starting medicine molecule.

    Returns:
        int: Number of distinct molecules that can be created
    """
    # Parse replacement rules from input
    # Each rule maps a source pattern (e.g., "H") to one or more replacement patterns (e.g., "HO", "OH")
    replacements = defaultdict(list)
    lines = AoCInput.read_lines(INPUT_FILE)

    # Read replacement rules until we hit the blank line
    for line in lines:
        if not line.strip():
            break
        source_pattern, replacement_pattern = line.strip().split(" => ")
        replacements[source_pattern].append(replacement_pattern)

    # The medicine molecule is the last line of the input
    medicine_molecule = lines[-1].strip()

    # Track all distinct molecules that can be created with one replacement
    distinct_molecules = set()

    # For each source pattern in our replacement rules
    for source_pattern in replacements:
        # Find all locations where this pattern appears in the molecule
        pattern_locations = [match.span() for match in re.finditer(source_pattern, medicine_molecule)]

        # For each location where the pattern appears
        for start_pos, end_pos in pattern_locations:
            # Try each possible replacement for this pattern
            for replacement_pattern in replacements[source_pattern]:
                # Create new molecule: prefix + replacement + suffix
                new_molecule = medicine_molecule[:start_pos] + replacement_pattern + medicine_molecule[end_pos:]
                distinct_molecules.add(new_molecule)

    return len(distinct_molecules)


answer = solve_part1()
AoCUtils.print_solution(1, answer)
