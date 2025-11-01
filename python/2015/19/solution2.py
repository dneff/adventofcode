import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/19/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
import re
from collections import defaultdict


# Memoization to track molecules we've already explored (prevents infinite loops)
visited_molecules = set()


def get_reverse_replacements(molecule, reverse_transforms):
    """
    Generate all possible molecules by applying reverse transformations.

    This works backwards: we replace complex patterns with simpler ones,
    trying to reduce the molecule back to 'e' (a single electron).

    Args:
        molecule: Current molecule string
        reverse_transforms: Dict mapping complex patterns to simpler replacements

    Returns:
        List of molecules that can be created by one reverse replacement
    """
    global visited_molecules

    new_molecules = set()

    # For each complex pattern that can be replaced
    for target_pattern in reverse_transforms:
        # Find all locations where this pattern appears in the molecule
        pattern_locations = [match.span() for match in re.finditer(target_pattern, molecule)]

        # For each location where the pattern appears
        for start_pos, end_pos in pattern_locations:
            # Try each possible reverse replacement (simpler pattern)
            for simpler_pattern in reverse_transforms[target_pattern]:
                # Create new molecule by replacing complex pattern with simpler one
                new_molecule = molecule[:start_pos] + simpler_pattern + molecule[end_pos:]

                # Only return molecules we haven't explored yet
                if new_molecule not in visited_molecules:
                    new_molecules.add(new_molecule)

    # Prioritize molecules that don't contain 'e' (to avoid premature termination)
    molecules_without_e = [mol for mol in new_molecules if "e" not in mol]
    if len(molecules_without_e) > 0:
        return molecules_without_e
    else:
        return list(new_molecules)


def find_fabrication_steps(current_molecule, target_molecule, reverse_transforms):
    """
    Recursively find the steps to fabricate a molecule by working backwards.

    We start with the target medicine molecule and work backwards to 'e',
    applying reverse transformations (replacing complex with simpler patterns).

    Args:
        current_molecule: The molecule we're currently at
        target_molecule: The molecule we're trying to reach (usually 'e')
        reverse_transforms: Dict mapping complex patterns to simpler ones

    Returns:
        List of molecules in the fabrication path, or False if no path found
    """
    global visited_molecules

    # Base case: we've reached the target (single electron 'e')
    if current_molecule == target_molecule:
        return [target_molecule]

    # Avoid infinite loops - don't revisit molecules
    if current_molecule in visited_molecules:
        return False

    visited_molecules.add(current_molecule)

    # Try all possible reverse replacements from current molecule
    for next_molecule in get_reverse_replacements(current_molecule, reverse_transforms):
        result = find_fabrication_steps(next_molecule, target_molecule, reverse_transforms)
        if result:
            # Found a path! Add current molecule to the beginning
            result.insert(0, current_molecule)
            return result

    return False


def solve_part2():
    """
    Solve Day 19 Part 2: Medicine for Rudolph - Molecule Fabrication

    Find the minimum number of steps to fabricate the medicine molecule
    starting from a single electron 'e', using the available replacements.

    This solution works backwards: starting from the medicine molecule and
    applying reverse transformations to reduce it back to 'e'.

    Returns:
        int: Minimum number of fabrication steps
    """
    # Build reverse transformation rules (complex pattern -> simpler pattern)
    # In forward direction: e => H means we can create H from e
    # In reverse direction: H => e means we can reduce H back to e
    reverse_replacements = defaultdict(list)
    lines = AoCInput.read_lines(INPUT_FILE)

    # Read replacement rules until we hit the blank line
    for line in lines:
        if not line.strip():
            break
        simpler_pattern, complex_pattern = line.strip().split(" => ")
        # Reverse the transformation: map complex pattern to simpler one
        reverse_replacements[complex_pattern].append(simpler_pattern)

    # The medicine molecule is the last line of the input
    medicine_molecule = lines[-1].strip()

    # Find the path from medicine molecule back to 'e' (single electron)
    fabrication_path = find_fabrication_steps(medicine_molecule, 'e', reverse_replacements)

    # Number of steps is the path length minus 1 (don't count the starting molecule)
    return len(fabrication_path) - 1

answer = solve_part2()
AoCUtils.print_solution(2, answer)
