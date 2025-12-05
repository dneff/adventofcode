"""
Advent of Code 2025 - Day 3: Lobby
https://adventofcode.com/2025/day/3

Part Two ---

There are batteries nearby that can supply emergency power to the escalator 
for just such an occasion. The batteries are each labeled with their joltage 
rating, a value from 1 to 9. You make a note of their joltage ratings (your 
puzzle input). For example:

987654321111111
811111111111119
234234234234278
818181911112111

The joltage output for the bank is still the number formed by the digits of 
the batteries you've turned on; the only difference is that now there will 
be 12 digits in each bank's joltage output instead of two.

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
    possible by turning on exactly twelve batteries.

    The strategy is to parse the battery ratings. If the current value is larger than a previous position,
    pop the previous value and add the current value to the list of turned-on batteries. For large values, 
    This may involve removing multiple previous values to ensure that only the highest values are kept.

    Be careful to turn on twelve batteries. If we're reaching the end of the list and haven't turned on twelve batteries yet,
    we may need to turn on some of the smaller batteries to reach the required count.

    Args:
        battery_line (str): A string of digits representing battery joltage ratings.

    Returns:
        int: The maximum joltage possible from the bank.
    """
    length = len(battery_line)
    batteries = [int(digit) for digit in battery_line]
    on_batteries = []

    for i in range(length):
        current_value = batteries[i]

        while   len(on_batteries) > 0 and \
                len(on_batteries) + (length - i) > 12 and \
                current_value > on_batteries[-1]:
            on_batteries.pop()
        
        if len(on_batteries) < 12:
            on_batteries.append(current_value)

    # convert battery list to joltage number
    joltage = int("".join(str(digit) for digit in on_batteries))
    return joltage



batteries = AoCInput.read_lines(INPUT_FILE)
total_joltage = [find_max_joltage(line) for line in batteries]
AoCUtils.print_solution(2, sum(total_joltage))
