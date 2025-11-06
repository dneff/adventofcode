import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/19/input')


def solve_part2():
    """
    Solve Day 19 Part 2: Medicine for Rudolph - Molecule Fabrication

    Find the minimum number of steps to fabricate the medicine molecule
    starting from a single electron 'e', using the available replacements.

    This solution uses a MATHEMATICAL FORMULA based on the structure of the
    replacement rules in the AoC input (discovered by askalski).

    Key Insight:
    The replacement rules follow a specific grammar structure:
    - e => X (start with single atom)
    - X => YZ (expand to two atoms)
    - X => Y Rn Z Ar (like Y(Z) with parentheses)
    - X => Y Rn Z Y W Ar (like Y(Z, W) with commas)

    Special tokens that only appear on the RIGHT side of rules:
    - Rn and Ar represent opening and closing parentheses
    - Y represents comma separators between sub-expressions

    Formula: num_atoms - num_Rn - num_Ar - (2 * num_Y) - 1

    Why it works:
    1. Without special tokens, n atoms require n-1 fabrication steps
       (each step adds exactly 1 atom, starting from e)
    2. Rn/Ar pairs add "extra" atoms that don't count as productive steps
       (they're structural markers, like parentheses)
    3. Y tokens add even more "extra" atoms (each Y represents a branch
       point that adds 2 atoms without needing 2 steps)
    4. The -1 accounts for starting from 'e' (zero atoms) to reach n atoms

    Returns:
        int: Minimum number of fabrication steps
    """
    lines = AoCInput.read_lines(INPUT_FILE)

    # The medicine molecule is the last line of the input
    medicine_molecule = lines[-1].strip()

    # Count atoms (each uppercase letter represents one atom/element)
    num_atoms = sum(1 for c in medicine_molecule if c.isupper())

    # Count special structural tokens
    num_rn = medicine_molecule.count("Rn")  # Opening "parentheses"
    num_ar = medicine_molecule.count("Ar")  # Closing "parentheses"
    num_y = medicine_molecule.count("Y")     # "Comma" separators

    # Apply the formula to calculate minimum fabrication steps
    fabrication_steps = num_atoms - num_rn - num_ar - (2 * num_y) - 1

    return fabrication_steps


answer = solve_part2()
AoCUtils.print_solution(2, answer)
