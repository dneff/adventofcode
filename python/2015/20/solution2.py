import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/20/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def get_divisors(house_number):
    """
    Get all divisors (factors) of a house number.

    In Part 2, each elf still delivers to houses that are multiples of their elf number,
    but only to the first 50 such houses. The elves that could visit a house are still
    the divisors of that house number (though some may have stopped before reaching it).

    For example, house 12 could be visited by elves: 1, 2, 3, 4, 6, 12
    (all divisors of 12), but only if house 12 is within each elf's 50-house limit.

    Args:
        house_number: The house number to find divisors for

    Returns:
        Set of all divisors (elf numbers that could visit this house)

    Note: This function is kept for consistency but not used in the optimized Part 2 solution.
    """
    divisors = []
    # Only need to check up to sqrt(house_number) for efficiency
    for i in range(1, int(house_number ** 0.5) + 1):
        if house_number % i == 0:
            # Add both the divisor and its complement
            divisors.extend([i, house_number // i])
    return set(divisors)


def solve_part2():
    """
    Find the lowest house number that receives at least the target number of presents.

    Part 2 Modified Rules:
    - Elf N delivers to every Nth house (houses N, 2N, 3N, ...) BUT stops after 50 houses
    - Each elf delivers 11 * (their elf number) presents to each house they visit (increased from 10x)
    - Total presents at a house = sum of (11 * elf_number) for all elves that visit before stopping

    Example: Elf 10 visits houses 10, 20, 30, ..., 500 (50 houses total) and delivers 110 presents each.
             Elf 10 does NOT visit house 510 or beyond.

    Optimization: Use a sieve approach where each elf "delivers" to their limited set of houses
    instead of computing divisors for each house. This is much faster.
    """
    # Read the target number of presents from the input file
    target_presents = int(AoCInput.read_lines(INPUT_FILE)[0])

    # Upper bound estimate: With 11x multiplier and 50 house limit, we need a reasonable search space.
    # Each elf N delivers 11*N presents to at most 50 houses. Using a conservative estimate.
    max_house = target_presents // 11

    # Initialize presents array - each house starts with 0 presents
    presents = [0] * (max_house + 1)

    # Track the minimum house number that has reached the target (optimization for early exit)
    min_possible_answer = max_house

    # Sieve approach: each elf delivers to their houses
    # Elf N delivers to houses: N, 2N, 3N, 4N, ... (up to 50 houses)
    for elf_number in range(1, max_house + 1):
        # Early exit: if current elf number is higher than our best answer found,
        # we can stop (no future house below our answer will get more presents)
        if elf_number > min_possible_answer:
            break

        # Part 2 change: Elf delivers 11 * elf_number presents (increased from 10x)
        presents_to_deliver = 11 * elf_number

        # Part 2 constraint: Each elf only visits the first 50 houses that are multiples of their number
        max_houses_per_elf = 50

        # Calculate the last house this elf will visit (50th multiple or our current best answer, whichever is lower)
        last_house_visited = min(elf_number * max_houses_per_elf, min_possible_answer)

        # Deliver presents to each house this elf visits
        for house in range(elf_number, last_house_visited + 1, elf_number):
            presents[house] += presents_to_deliver

            # Check if this house just reached the target
            if presents[house] >= target_presents and house < min_possible_answer:
                min_possible_answer = house

    # Return the answer we found
    return min_possible_answer if min_possible_answer < max_house else None

answer = solve_part2()
AoCUtils.print_solution(2, answer)
