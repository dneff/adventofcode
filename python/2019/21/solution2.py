"""
Advent of Code 2019 - Day 21: Springdroid Adventure

Part 1: Program the springdroid to jump over holes in the hull.

Program the springdroid with logic that allows it to survey
the hull without falling into space.

What amount of hull damage does it report?
"""

import os
import sys
import re

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "../../"))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402
from springbotOS import IntCode, OutputInterrupt  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, "../../../../aoc-data/2019/21/input")

# Parse the input to understand the hull layout (if provided in the output)
springdroid_system = AoCInput.read_file(INPUT_FILE).strip()

springdroid = IntCode(springdroid_system)

"""
There are only three instructions available in springscript:
    AND X Y sets Y to true if both X and Y are true; otherwise, it sets Y to false.
    OR X Y sets Y to true if at least one of X or Y is true; otherwise, it sets Y to false.
    NOT X Y sets Y to true if X is false; otherwise, it sets Y to false.

complete program must be 15 instructions or fewer    

sensor  A B C D E F G H I detect hull (ground/hole)
register J T are writable temporary registers

Springdroid jumps if register J is true at the time of the jump (move forward 4 steps),
else it walks (move forward 1 step).

Strategy:
Jump if:
    There's a hole in A, B, or C (immediate danger)
    D is safe (landing spot)
    AND at least one of these is true:
        E is safe (you can walk from D)
        H is safe (you can jump from D+1 and land safely on H)
"""

program = [
    "NOT C J",    # J = !C
    "NOT B T",    # T = !B
    "OR T J",     # J = !B || !C
    "NOT A T",    # T = !A
    "OR T J",     # J = !A || !B || !C
    "AND D J",    # J = (!A || !B || !C) && D
    "OR E T",     # T = !A || E
    "OR H T",     # T = !A || E || H
    "AND T J",    # J = ((!A || !B || !C) && D) && (!A || E || H)
    "RUN"
]

# Convert program to ASCII input
ascii_input = [ord(c) for line in program for c in line + "\n"]
for code in ascii_input:
    springdroid.push(code)

# Debugging flag to generate ASCII output
springdroid.debugging = False

springdroid_output = []
ascii_buffer = []

while not springdroid.complete:
    try:
        springdroid.run()
    except OutputInterrupt:
        while springdroid.output:
            value = springdroid.pop()
            springdroid_output.append(value)

for output in springdroid_output:
    if output < 128:
        ascii_buffer.append(chr(output))
    else:
        # Non-ASCII output indicates hull damage
        pass

print("".join(ascii_buffer))

# The last output value is the hull damage reported
AoCUtils.print_solution(2, springdroid_output[-1])
