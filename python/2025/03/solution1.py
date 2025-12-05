"""
Advent of Code 2025 - Day 3: Lobby
https://adventofcode.com/2025/day/3

Part ONE ---

There are batteries nearby that can supply emergency power to the escalator 
for just such an occasion. The batteries are each labeled with their joltage 
rating, a value from 1 to 9. You make a note of their joltage ratings (your 
puzzle input). For example:

987654321111111
811111111111119
234234234234278
818181911112111

The batteries are arranged into banks; each line of digits in your input 
corresponds to a single bank of batteries. Within each bank, you need to 
turn on exactly two batteries; the joltage that the bank produces is equal 
to the number formed by the digits on the batteries you've turned on. For 
example, if you have a bank like 12345 and you turn on batteries 2 and 4, 
the bank would produce 24 jolts. (You cannot rearrange batteries.)

There are many batteries in front of you. Find the maximum
joltage possible from each bank; what is the total output joltage?

"""

import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "../../"))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, "../../../../aoc-data/2025/3/input")

def find_max_joltage(battery_line):
    """
    Given a line of battery joltage ratings, find the maximum joltage 
    possible by turning on exactly two batteries.

    Args:
        battery_line (str): A string of digits representing battery joltage ratings.

    Returns:
        int: The maximum joltage possible from the bank.
    """
    length = len(battery_line)

    batteries = [int(digit) for digit in battery_line]
    first_battery = max(batteries[:-1])
    first_battery_index = batteries.index(first_battery)
    second_battery = max(batteries[first_battery_index + 1 :])

    return 10 * first_battery + second_battery


batteries = AoCInput.read_lines(INPUT_FILE)

total_joltage = sum(find_max_joltage(line) for line in batteries)

AoCUtils.print_solution(1, total_joltage)
