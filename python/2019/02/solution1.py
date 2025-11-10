"""
Advent of Code 2019 - Day 2: 1202 Program Alarm
Part 1: Restore the gravity assist program and run the Intcode computer.

The Intcode program is a list of integers separated by commas. The computer
processes opcodes:
- Opcode 1: Add values from two positions, store in third position
- Opcode 2: Multiply values from two positions, store in third position
- Opcode 99: Halt the program

For the "1202 program alarm" state, restore:
- Position 1 = 12 (noun)
- Position 2 = 2 (verb)

Then run the program and report the value at position 0.
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


def solve_part1():
    """
    Restore the gravity assist program to the 1202 alarm state and run it.

    The 1202 program alarm means:
    - Set position 1 (noun) to 12
    - Set position 2 (verb) to 2
    """
    content = AoCInput.read_file(INPUT_FILE)
    memory = [int(x) for x in content.strip().split(',')]

    # Restore the "1202 program alarm" state
    memory[1] = 12  # noun
    memory[2] = 2   # verb

    return run_intcode_program(memory)


answer = solve_part1()
AoCUtils.print_solution(1, answer)