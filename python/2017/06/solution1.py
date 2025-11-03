"""
Advent of Code 2017 - Day 6: Memory Reallocation (Part 1)

Detect infinite loops in a memory reallocation routine. The routine redistributes blocks from
the bank with the most blocks to subsequent banks in circular fashion. Count how many
redistribution cycles occur before a configuration repeats.

Example:
    Starting with [0, 2, 7, 0]:
    - After 5 cycles, the configuration [2, 4, 1, 2] appears for the second time
    - Answer: 5 cycles
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/6/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


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
    """Count redistribution cycles until a configuration repeats."""
    line = AoCInput.read_lines(INPUT_FILE)[0]
    memory_banks = [int(x) for x in line.strip().split()]

    seen_configurations = set()
    seen_configurations.add(tuple(memory_banks))

    cycles = 0
    current_banks = reallocate_memory(memory_banks)
    cycles += 1

    while tuple(current_banks) not in seen_configurations:
        seen_configurations.add(tuple(current_banks))
        current_banks = reallocate_memory(current_banks)
        cycles += 1

    AoCUtils.print_solution(1, cycles)
    


if __name__ == "__main__":
    main()