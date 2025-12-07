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

Part 2

Cephalopod math is written right-to-left in columns. Each number is given in
its own column, with the most significant digit at the top and the least 
significant digit at the bottom. (Problems are still separated with a column 
consisting only of spaces, and the symbol at the bottom of the problem is 
still the operator to use.)

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

# Read input preserving leading spaces (important for column alignment)
worksheet_rows = AoCInput.read_lines(INPUT_FILE, preserve_leading_space=True)

# Parse problems from the worksheet
# In Part 2, each number is written vertically in its own column:
# - Most significant digit at the top
# - Least significant digit at the bottom
# - Operator symbol at the very bottom
# - Problems are separated by blank columns (all spaces)
problems = []
current_operator = ''
current_number_digits = []  # List of digits (each digit is read from one column)

for col_index in range(len(worksheet_rows[0])):
    # Extract the column: read vertically down all rows for this column
    column_chars = [row[col_index] for row in worksheet_rows]

    # Check if this is a blank column (separator between problems)
    if all(char == ' ' for char in column_chars):
        # Save the completed problem if we have valid data
        if current_number_digits and current_operator in ('+', '*'):
            problems.append((current_number_digits, current_operator))
            current_number_digits = []
            current_operator = ''
        continue

    # Check if the last row has an operator
    if column_chars[-1] in ('+', '*'):
        current_operator = column_chars[-1]

    # Read the digit from this column (all rows except the last, which has the operator)
    # Join the characters vertically to form a multi-digit number
    digit = int(''.join(column_chars[:-1]))
    current_number_digits.append(digit)

# Save any remaining problem at the end of the worksheet
if current_number_digits and current_operator in ('+', '*'):
    problems.append((current_number_digits, current_operator))

# Solve each problem
problem_answers = []
for numbers, operator in problems:
    # Calculate result based on the operator
    if operator == '+':
        result = sum(numbers)
    elif operator == '*':
        result = reduce(mul, numbers, 1)

    problem_answers.append(result)

# The grand total is the sum of all individual problem answers
grand_total = sum(problem_answers)
AoCUtils.print_solution(2, grand_total)
