"""
Advent of Code 2019 - Day 2: 1202 Program Alarm
Part 2: Find the noun and verb that produce a specific output.

"Good, the new computer seems to be working correctly! Keep it nearby during
this mission - you'll probably use it again. Real Intcode computers support
many more features than your new one, but we'll let you know what they are
as you need them."

"However, your current priority should be to complete your gravity assist
around the Moon. For this mission to succeed, we should settle on some
terminology for the parts you've already built."

The inputs (positions 1 and 2) are called the "noun" and "verb". Each can
be a value from 0 to 99. Find the noun and verb that cause the program to
produce the output 19690720.

The answer is: 100 * noun + verb
"""
import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/2/input')


def execute_add(parameters, memory):
    """
    Execute addition opcode: memory[params[2]] = memory[params[0]] + memory[params[1]]

    Args:
        parameters: List of 3 positions [input1_pos, input2_pos, output_pos]
        memory: The Intcode program memory
    """
    memory[parameters[2]] = memory[parameters[0]] + memory[parameters[1]]


def execute_multiply(parameters, memory):
    """
    Execute multiplication opcode: memory[params[2]] = memory[params[0]] * memory[params[1]]

    Args:
        parameters: List of 3 positions [input1_pos, input2_pos, output_pos]
        memory: The Intcode program memory
    """
    memory[parameters[2]] = memory[parameters[0]] * memory[parameters[1]]


def run_intcode_program(memory):
    """
    Run the Intcode program until it halts.

    Args:
        memory: The Intcode program memory (will be modified in place)

    Returns:
        The value at position 0 after the program halts
    """
    instruction_pointer = 0

    while True:
        opcode = memory[instruction_pointer]

        if opcode == 99:  # Halt
            break
        elif opcode == 1:  # Add
            parameters = memory[instruction_pointer + 1:instruction_pointer + 4]
            execute_add(parameters, memory)
        elif opcode == 2:  # Multiply
            parameters = memory[instruction_pointer + 1:instruction_pointer + 4]
            execute_multiply(parameters, memory)

        instruction_pointer += 4  # Move to next instruction

    return memory[0]


def solve_part2():
    """
    Find the noun and verb that produce the target output 19690720.

    Brute force search through all possible combinations of noun (0-99)
    and verb (0-99) to find the pair that produces the desired output.

    Returns:
        100 * noun + verb for the successful pair
    """
    content = AoCInput.read_file(INPUT_FILE)
    initial_memory = [int(x) for x in content.strip().split(',')]

    target_output = 19690720

    # Try all combinations of noun and verb (0-99 each)
    for noun in range(100):
        for verb in range(100):
            # Create a fresh copy of memory for each test
            test_memory = initial_memory[:]
            test_memory[1] = noun
            test_memory[2] = verb

            output = run_intcode_program(test_memory)

            if output == target_output:
                # Found the answer: 100 * noun + verb
                return 100 * noun + verb

    return None


answer = solve_part2()
AoCUtils.print_solution(2, answer)