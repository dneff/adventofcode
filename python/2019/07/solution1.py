"""
Advent of Code 2019 - Day 7: Amplification Circuit - Part 1

Find the maximum thruster signal by connecting five amplifiers in series.
Each amplifier runs the Intcode program with a unique phase setting (0-4)
and a signal input. Test all permutations of phase settings to find the
configuration that produces the highest output signal to the thrusters.
"""
import os
import sys
from itertools import permutations

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/7/input')


def advance_instruction_pointer(pointer, size):
    """Advance the instruction pointer by the specified size."""
    return pointer + size


def get_parameter_modes(mode_value):
    """
    Convert mode value into parameter modes for up to 2 parameters.
    Mode 0 = position mode, Mode 1 = immediate mode
    """
    modes = {
        0: [0, 0],
        1: [1, 0],
        10: [0, 1],
        11: [1, 1]
    }
    return modes[mode_value]


def resolve_parameters(parameters, modes, memory):
    """Resolve parameters based on their modes (position or immediate)."""
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


def run_amplifier(memory, *inputs):
    """
    Run an amplifier program with the given inputs.

    Args:
        memory: The Intcode program
        *inputs: Variable number of inputs (phase setting, then signal)

    Returns:
        The output signal from the amplifier
    """
    instruction_pointer = 0
    input_values = list(reversed(inputs))  # Reverse for easier pop()
    outputs = []

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
            execute_input(memory[instruction_pointer + 1], input_values.pop(), memory)
            instruction_pointer = advance_instruction_pointer(instruction_pointer, 2)
        elif opcode == 4:
            # Output
            outputs.append(execute_output(memory[instruction_pointer + 1], memory))
            instruction_pointer = advance_instruction_pointer(instruction_pointer, 2)
        elif opcode == 5:
            # Jump-if-true
            params = resolve_parameters(
                memory[instruction_pointer + 1: instruction_pointer + 3],
                parameter_modes,
                memory
            )
            if params[0] != 0:
                instruction_pointer = params[1]
            else:
                instruction_pointer = advance_instruction_pointer(instruction_pointer, 3)
        elif opcode == 6:
            # Jump-if-false
            params = resolve_parameters(
                memory[instruction_pointer + 1: instruction_pointer + 3],
                parameter_modes,
                memory
            )
            if params[0] == 0:
                instruction_pointer = params[1]
            else:
                instruction_pointer = advance_instruction_pointer(instruction_pointer, 3)
        elif opcode == 7:
            # Less than
            params = resolve_parameters(
                memory[instruction_pointer + 1: instruction_pointer + 4],
                parameter_modes,
                memory
            )
            if params[0] < params[1]:
                memory[params[2]] = 1
            else:
                memory[params[2]] = 0
            instruction_pointer = advance_instruction_pointer(instruction_pointer, 4)
        elif opcode == 8:
            # Equals
            params = resolve_parameters(
                memory[instruction_pointer + 1: instruction_pointer + 4],
                parameter_modes,
                memory
            )
            if params[0] == params[1]:
                memory[params[2]] = 1
            else:
                memory[params[2]] = 0
            instruction_pointer = advance_instruction_pointer(instruction_pointer, 4)

    return outputs.pop()


def solve_part1():
    """Find maximum thruster signal from all phase setting permutations."""
    content = AoCInput.read_file(INPUT_FILE)
    amplifier_program = [int(x) for x in content.strip().split(',')]

    max_thruster_signal = 0
    phase_settings = [0, 1, 2, 3, 4]

    # Try all permutations of phase settings
    for phase_sequence in permutations(phase_settings):
        signal = 0
        # Run signal through amplifiers A->B->C->D->E
        for phase in phase_sequence:
            signal = run_amplifier(amplifier_program[:], phase, signal)
        max_thruster_signal = max(max_thruster_signal, signal)

    return max_thruster_signal


answer = solve_part1()
AoCUtils.print_solution(1, answer)