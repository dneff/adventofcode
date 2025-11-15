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

# Springdroid program to jump over holes
program = ["NOT A J", "NOT B T", "OR T J", "NOT C T", "OR T J", "AND D J", "WALK"]

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
        value = springdroid.pop()
        springdroid_output.append(value)

# The last output value is the hull damage reported
AoCUtils.print_solution(1, springdroid_output[-1])
