"""
Advent of Code 2017 - Day 6: Memory Reallocation (Part 2)

Find the size of the infinite loop. After detecting when a configuration repeats, determine
how many cycles are in the loop between the first and second occurrence of that configuration.

Example:
    Starting with [0, 2, 7, 0]:
    - Configuration [2, 4, 1, 2] first appears after 1 cycle
    - It appears again after 5 cycles
    - Loop size: 5 - 1 = 4
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/6/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402
from collections import defaultdict  # noqa: E402


def reallocate_memory(memory_banks):
    """
    Redistribute blocks from the fullest bank to subsequent banks.

    Args:
        memory_banks: List of integers representing blocks in each bank

    Returns:
        New memory bank configuration after reallocation
    """
    banks = memory_banks[:]
    # Find the bank with the most blocks (ties go to lowest index)
    max_index = banks.index(max(banks))
    blocks_to_distribute = banks[max_index]
    banks[max_index] = 0

    # Distribute blocks one at a time in circular fashion
    current_index = max_index
    while blocks_to_distribute > 0:
        current_index = (current_index + 1) % len(banks)
        banks[current_index] += 1
        blocks_to_distribute -= 1

    return banks


def main():
    """Calculate the size of the infinite loop."""
    line = AoCInput.read_lines(INPUT_FILE)[0]
    memory_banks = [int(x) for x in line.strip().split()]

    seen_configurations = set()
    configuration_cycle_map = defaultdict(list)

    cycles = 0
    seen_configurations.add(tuple(memory_banks))
    configuration_cycle_map[tuple(memory_banks)].append(cycles)

    current_banks = reallocate_memory(memory_banks)
    cycles += 1

    while tuple(current_banks) not in seen_configurations:
        seen_configurations.add(tuple(current_banks))
        configuration_cycle_map[tuple(current_banks)].append(cycles)

        current_banks = reallocate_memory(current_banks)
        cycles += 1

    # Loop size is current cycle minus the cycle when this configuration first appeared
    first_occurrence = configuration_cycle_map[tuple(current_banks)][0]
    loop_size = cycles - first_occurrence

    AoCUtils.print_solution(2, loop_size)


if __name__ == "__main__":
    main()
