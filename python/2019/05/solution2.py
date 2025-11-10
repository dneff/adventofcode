"""
Advent of Code 2019 - Day 5: Sunny with a Chance of Asteroids - Part 2

Run the TEST diagnostic program on the Intcode computer with input value 5
(for thermal radiator controller system). This part adds new comparison and jump
instructions (opcodes 5-8) to handle more complex control flow:
- Opcode 5: jump-if-true
- Opcode 6: jump-if-false
- Opcode 7: less than
- Opcode 8: equals
"""
import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/5/input')


def advance_instruction_pointer(pointer, size):
    """Advance the instruction pointer by the specified size."""
    return pointer + size


def get_parameter_modes(mode_value):
    """
    Convert mode value into parameter modes for up to 2 parameters.
    Mode 0 = position mode (parameter is address)
    Mode 1 = immediate mode (parameter is value)
    """
    modes = {
        0: [0, 0],
        1: [1, 0],
        10: [0, 1],
        11: [1, 1]
    }
    return modes[mode_value]


def resolve_parameters(parameters, modes, memory):
    """
    Resolve parameters based on their modes.
    Position mode (0): parameter is address, fetch value from that address
    Immediate mode (1): parameter is the value itself
    """
    resolved = parameters[:]
    for idx, mode in enumerate(modes):
        if mode == 0:
            resolved[idx] = memory[parameters[idx]]
        elif mode == 1:
            resolved[idx] = parameters[idx]
    return resolved


def execute_add(parameters, memory):
    """Add two values and store in third parameter address."""
    memory[parameters[2]] = parameters[0] + parameters[1]


def execute_multiply(parameters, memory):
    """Multiply two values and store in third parameter address."""
    memory[parameters[2]] = parameters[0] * parameters[1]


def execute_input(address, input_value, memory):
    """Store input value at the specified address."""
    memory[address] = input_value


def execute_output(address, memory):
    """Return the value at the specified address."""
    return memory[address]


def execute_jump_if_true(parameters, instruction_pointer):
    """
    Jump to address if first parameter is non-zero.
    Returns new instruction pointer.
    """
    if parameters[0] != 0:
        return parameters[1]
    else:
        return advance_instruction_pointer(instruction_pointer, 3)


def execute_jump_if_false(parameters, instruction_pointer):
    """
    Jump to address if first parameter is zero.
    Returns new instruction pointer.
    """
    if parameters[0] == 0:
        return parameters[1]
    else:
        return advance_instruction_pointer(instruction_pointer, 3)


def execute_less_than(parameters, memory):
    """Store 1 if first parameter < second parameter, else 0."""
    if parameters[0] < parameters[1]:
        memory[parameters[2]] = 1
    else:
        memory[parameters[2]] = 0


def execute_equals(parameters, memory):
    """Store 1 if first parameter == second parameter, else 0."""
    if parameters[0] == parameters[1]:
        memory[parameters[2]] = 1
    else:
        memory[parameters[2]] = 0


def run_diagnostic_program(memory, system_id):
    """
    Run the TEST diagnostic program with the given system ID.

    Args:
        memory: The Intcode program as a list of integers
        system_id: The system ID to provide as input (5 for thermal radiator controller)

    Returns:
        The final diagnostic code (last output value)
    """
    instruction_pointer = 0
    diagnostic_outputs = []

    while True:
        modes, opcode = divmod(memory[instruction_pointer], 100)
        parameter_modes = get_parameter_modes(modes)

        if opcode == 99:
            # Halt
            break
        elif opcode == 1:
            # Add
            params = resolve_parameters(
                memory[instruction_pointer + 1: instruction_pointer + 4],
                parameter_modes,
                memory
            )
            execute_add(params, memory)
            instruction_pointer = advance_instruction_pointer(instruction_pointer, 4)
        elif opcode == 2:
            # Multiply
            params = resolve_parameters(
                memory[instruction_pointer + 1: instruction_pointer + 4],
                parameter_modes,
                memory
            )
            execute_multiply(params, memory)
            instruction_pointer = advance_instruction_pointer(instruction_pointer, 4)
        elif opcode == 3:
            # Input
            execute_input(memory[instruction_pointer + 1], system_id, memory)
            instruction_pointer = advance_instruction_pointer(instruction_pointer, 2)
        elif opcode == 4:
            # Output
            diagnostic_outputs.append(execute_output(memory[instruction_pointer + 1], memory))
            instruction_pointer = advance_instruction_pointer(instruction_pointer, 2)
        elif opcode == 5:
            # Jump-if-true
            params = resolve_parameters(
                memory[instruction_pointer + 1: instruction_pointer + 3],
                parameter_modes,
                memory
            )
            instruction_pointer = execute_jump_if_true(params, instruction_pointer)
        elif opcode == 6:
            # Jump-if-false
            params = resolve_parameters(
                memory[instruction_pointer + 1: instruction_pointer + 3],
                parameter_modes,
                memory
            )
            instruction_pointer = execute_jump_if_false(params, instruction_pointer)
        elif opcode == 7:
            # Less than
            params = resolve_parameters(
                memory[instruction_pointer + 1: instruction_pointer + 4],
                parameter_modes,
                memory
            )
            execute_less_than(params, memory)
            instruction_pointer = advance_instruction_pointer(instruction_pointer, 4)
        elif opcode == 8:
            # Equals
            params = resolve_parameters(
                memory[instruction_pointer + 1: instruction_pointer + 4],
                parameter_modes,
                memory
            )
            execute_equals(params, memory)
            instruction_pointer = advance_instruction_pointer(instruction_pointer, 4)

    return diagnostic_outputs[-1] if diagnostic_outputs else memory[0]


def solve_part2():
    """Run TEST diagnostic program for thermal radiator controller (system ID 5)."""
    content = AoCInput.read_file(INPUT_FILE)
    diagnostic_program = [int(x) for x in content.strip().split(',')]

    return run_diagnostic_program(diagnostic_program, 5)


answer = solve_part2()
AoCUtils.print_solution(2, answer)
