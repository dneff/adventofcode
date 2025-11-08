"""
Advent of Code 2018 - Day 21: Chronal Conversion (Part 2) - Optimized
https://adventofcode.com/2018/day/21

This is a reverse-engineered version of the assembly program that runs
thousands of times faster by implementing the algorithm directly instead
of simulating all the opcode instructions.

The program generates a sequence of values in r5 and checks at instruction 28
if r5 == r0. We want to find the last unique r5 value before the sequence repeats.
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCUtils

def generate_r5_sequence():
    """
    Reverse-engineered algorithm from the assembly code.

    The program computes a hash-like sequence:
    - Line 6: r3 = r5 | 65536
    - Line 7: r5 = 10828530
    - Lines 8-12: Process lowest byte of r3 into r5
    - Lines 13-27: Divide r3 by 256 and repeat
    - Line 28: Check if r5 == r0 (halt condition)

    This generates r5 values until we see a repeat.
    """
    seen = set()
    r5_values = []
    r5 = 0

    while True:
        # Start of main loop (instruction 6)
        r3 = r5 | 65536
        r5 = 10828530

        while True:
            # Process one byte of r3 (instructions 8-12)
            r2 = r3 & 255  # Get lowest byte
            r5 = (r5 + r2) & 16777215  # Add and mask to 24 bits
            r5 = (r5 * 65899) & 16777215  # Multiply and mask to 24 bits

            # Check if r3 < 256 (instruction 13)
            if r3 < 256:
                # This is where we reach instruction 28 and check r5 == r0
                if r5 in seen:
                    # We've seen this r5 before - the sequence is repeating
                    return r5_values

                seen.add(r5)
                r5_values.append(r5)
                print(f"Found r5 value #{len(r5_values)}: {r5}")
                break

            # Divide r3 by 256 (instructions 17-25)
            # The assembly does this with a loop, but we can just divide
            r3 = r3 // 256

def main():
    print("Generating r5 sequence (optimized algorithm)...")
    print("This finds all unique r5 values before the first repeat.\n")

    r5_values = generate_r5_sequence()

    print(f"\nTotal unique r5 values: {len(r5_values)}")
    print(f"First r5 value (Part 1): {r5_values[0]}")
    print(f"Last r5 value (Part 2): {r5_values[-1]}")

    AoCUtils.print_solution(2, r5_values[-1])

if __name__ == '__main__':
    main()
