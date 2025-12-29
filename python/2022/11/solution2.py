"""
Advent of Code 2022 - Day 11, Part 2
https://adventofcode.com/2022/day/11

This script simulates monkeys for 10000 rounds without worry relief.
"""

import os
import sys
from math import prod

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2022/11/input')


class Monkey:
    """Represents a monkey with items and behavior."""

    def __init__(self):
        self.items = []
        self.operator = ""
        self.relief = 1
        self.test_val = 1
        self.test_true = 1
        self.test_false = 0
        self.inspect_count = 0
        self.max_val = 0

    def worry(self, old):
        """Calculate new worry level using modular arithmetic."""
        new = eval(self.operator) // self.relief
        return new % self.max_val

    def inspect(self, item):
        """Determine which monkey gets the item."""
        if item % self.test_val == 0:
            return self.test_true
        return self.test_false

    def turn(self, monkeys):
        """Process all items during this monkey's turn."""
        while self.items:
            self.inspect_count += 1
            item = self.items.pop()
            item = self.worry(item)
            monkeys[self.inspect(item)].items.append(item)


def solve_part2():
    """
    Simulate monkeys for 10000 rounds and calculate monkey business.

    Returns:
        int: Product of top 2 monkey inspection counts
    """
    lines = AoCInput.read_lines(INPUT_FILE)

    monkeys = []
    for line in lines:
        if line.startswith('Monkey'):
            monkeys.append(Monkey())
        elif 'Starting' in line:
            monkeys[-1].items = [int(x) for x in line.split(': ')[-1].split(',')]
        elif 'Operation' in line:
            monkeys[-1].operator = line.split('= ')[-1]
        elif 'Test' in line:
            monkeys[-1].test_val = int(line.split('by ')[-1])
        elif 'true' in line:
            monkeys[-1].test_true = int(line.split('monkey ')[-1])
        elif 'false' in line:
            monkeys[-1].test_false = int(line.split('monkey ')[-1])

    # Calculate LCM of all test values for modular arithmetic
    max_val = prod([monkey.test_val for monkey in monkeys])
    for monkey in monkeys:
        monkey.max_val = max_val

    # Run 10000 rounds
    rounds = 10000
    for _ in range(rounds):
        for monkey in monkeys:
            monkey.turn(monkeys)

    # Calculate monkey business
    monkey_business = [monkey.inspect_count for monkey in monkeys]
    monkey_business.sort()

    return monkey_business[-1] * monkey_business[-2]


# Compute and print the answer for part 2
answer = solve_part2()
AoCUtils.print_solution(2, answer)
