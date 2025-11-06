import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/20/input')


def get_divisors(house_number):
    """
    Get all divisors (factors) of a house number.

    Each elf delivers to houses that are multiples of their elf number,
    so the elves visiting a house are exactly the divisors of that house number.

    For example, house 12 is visited by elves: 1, 2, 3, 4, 6, 12
    (all divisors of 12)

    Args:
        house_number: The house number to find divisors for

    Returns:
        Set of all divisors (elf numbers that visit this house)
    """
    divisors = []
    # Only need to check up to sqrt(house_number) for efficiency
    for i in range(1, int(house_number ** 0.5) + 1):
        if house_number % i == 0:
            # Add both the divisor and its complement
            divisors.extend([i, house_number // i])
    return set(divisors)


def solve_part1():
    """
    Find the lowest house number that receives at least the target number of presents.

    Rules:
    - Elf N delivers to every Nth house (houses N, 2N, 3N, ...)
    - Each elf delivers 10 * (their elf number) presents to each house they visit
    - Total presents at a house = sum of (10 * elf_number) for all visiting elves

    Optimization: Use a sieve approach where each elf "delivers" to all their houses
    instead of computing divisors for each house. This is much faster.
    We also use a more conservative upper bound to reduce memory and computation.
    """
    # Read the target number of presents from the input file
    target_presents = int(AoCInput.read_lines(INPUT_FILE)[0])

    # Better upper bound estimate: Based on highly composite numbers and the fact that
    # sum of divisors σ(n) can be quite large for numbers with many small prime factors.
    # Empirically, we need far less than target/10. Using target/30 as a safer estimate
    # that still captures highly composite numbers in the search space.
    max_house = target_presents // 30

    # Initialize presents array - each house starts with 0 presents
    presents = [0] * (max_house + 1)

    # Track the minimum house number that could still win (optimization for early exit)
    min_possible_answer = max_house

    # Sieve approach: each elf delivers to all their houses
    # Elf N delivers to houses: N, 2N, 3N, 4N, ...
    for elf_number in range(1, max_house + 1):
        # Early exit: if current elf number is higher than our best answer found,
        # we can stop (no future house below our answer will get more presents)
        if elf_number > min_possible_answer:
            break

        # Elf delivers 10 * elf_number presents to each house they visit
        presents_to_deliver = 10 * elf_number

        # Deliver to all houses that are multiples of elf_number
        for house in range(elf_number, min_possible_answer + 1, elf_number):
            presents[house] += presents_to_deliver

            # Check if this house just reached the target
            if presents[house] >= target_presents and house < min_possible_answer:
                min_possible_answer = house

    # Return the answer we found
    return min_possible_answer if min_possible_answer < max_house else None


answer = solve_part1()
AoCUtils.print_solution(1, answer)
