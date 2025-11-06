import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402
from itertools import combinations  # noqa: E402
from functools import reduce  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/24/input')


def solve_part1():
    """
    Solve Day 24 Part 1: It Hangs in the Balance

    Santa needs to balance packages on his sleigh by dividing them into 3 groups
    of equal weight. The first group (passenger compartment) must have the fewest
    packages possible. If multiple configurations have the same minimum package count,
    choose the one with the lowest quantum entanglement (product of package weights).

    Returns:
        The quantum entanglement of the ideal first group configuration
    """
    lines = AoCInput.read_lines(INPUT_FILE)
    package_weights = [int(x) for x in lines]

    # Each of the 3 groups must weigh exactly 1/3 of the total
    target_weight = sum(package_weights) // 3

    # Find the maximum possible size for the first group (passenger compartment)
    # This occurs when we take the lightest packages until we exceed the target
    max_packages_in_group = 1
    while sum(package_weights[:max_packages_in_group]) <= target_weight:
        max_packages_in_group += 1

    # Find the minimum possible size for the first group
    # This occurs when we take the heaviest packages until we exceed the target
    min_packages_in_group = 1
    while sum(package_weights[-min_packages_in_group:]) <= target_weight:
        min_packages_in_group += 1

    # Find combinations starting with the smallest group size
    # Once we find valid combinations of size N, that's our minimum, so we can stop
    for group_size in range(min_packages_in_group, max_packages_in_group + 1):
        # Track the minimum quantum entanglement for this group size
        min_quantum_entanglement = None

        package_combinations = combinations(package_weights, group_size)
        for combo in package_combinations:
            if sum(combo) == target_weight:
                # Calculate quantum entanglement (product of all package weights)
                qe = reduce((lambda a, b: a * b), combo)

                if min_quantum_entanglement is None or qe < min_quantum_entanglement:
                    min_quantum_entanglement = qe

        # If we found valid combinations for this size, return the minimum QE
        # No need to check larger group sizes since we want the minimum package count
        if min_quantum_entanglement is not None:
            return min_quantum_entanglement

    # Should never reach here with valid input
    return None


answer = solve_part1()
AoCUtils.print_solution(1, answer)
