"""
Advent of Code 2025 - Day 6: Trash Compactor
https://adventofcode.com/2025/day/6

Help the youngest cephalopod with her math homework.

Cephalopod math doesn't look that different from normal math. The math 
worksheet (your puzzle input) consists of a list of problems; each problem 
has a group of numbers that need to be either added (+) or multiplied (*) 
together.

However, the problems are arranged a little strangely; they seem to be 
presented next to each other in a very long horizontal list.

Part 1

Solve the problems on the math worksheet. What is the grand total found 
by adding together all of the answers to the individual problems?

"""

import os
import sys
from functools import reduce
from operator import mul

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "../../"))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, "../../../../aoc-data/2025/6/input")

# Parse input: each line becomes a list of tokens (numbers and operators)
# The problems are arranged horizontally, so each column is one problem
worksheet_rows = [line.split() for line in AoCInput.read_lines(INPUT_FILE)]

# Solve each problem (represented by a column in the worksheet)
problem_answers = []
num_problems = len(worksheet_rows[0])

for col_index in range(num_problems):
    # Extract the column: read vertically down all rows for this column index
    # Last element is the operator (+/*), all other elements are numbers
    column = [row[col_index] for row in worksheet_rows]

    # Parse the problem: numbers are all elements except the last (operator)
    numbers = [int(value) for value in column[:-1]]
    operator = column[-1]

    # Calculate result based on the operator
    if operator == '+':
        result = sum(numbers)
    elif operator == '*':
        result = reduce(mul, numbers, 1)

    problem_answers.append(result)

# The grand total is the sum of all individual problem answers
grand_total = sum(problem_answers)
AoCUtils.print_solution(1, grand_total)
