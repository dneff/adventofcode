"""
Advent of Code 2015 - Day 7: Some Assembly Required
https://adventofcode.com/2015/day/7

Simulates a circuit of wires and bitwise logic gates. Each wire carries a 16-bit signal
(0-65535). The circuit is defined by instructions that describe how signals are computed
using bitwise operations: AND, OR, LSHIFT, RSHIFT, and NOT.

Goal: Determine what signal is ultimately provided to wire 'a'.
"""

import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/7/input')


class Circuit:
    """
    Represents a circuit simulator that processes wire instructions.

    Wires can receive signals from:
    - Direct values (e.g., "123 -> x")
    - Other wires (e.g., "x -> y")
    - Bitwise operations (AND, OR, LSHIFT, RSHIFT, NOT)
    """
    def __init__(self):
        # Dictionary mapping wire names to their current signal values (16-bit integers)
        self.wire_signals = {}

    def has_signal(self, *wire_or_values):
        """
        Verify that all inputs are ready (either numeric values or wires with known signals).

        Args:
            *wire_or_values: Wire names or numeric strings to check

        Returns:
            bool: True if all inputs are available, False otherwise
        """
        for input_value in wire_or_values:
            # Check if input is not a literal int, not numeric, and not a wire with a known signal
            if (not isinstance(input_value, int) and not input_value.isnumeric() and
                    input_value not in self.wire_signals):
                return False
        return True

    def AND(self, left_input, right_input):
        """
        Perform bitwise AND operation on two inputs.

        Args:
            left_input: Wire name or numeric string
            right_input: Wire name or numeric string

        Returns:
            int: Bitwise AND result

        Raises:
            ValueError: If either input wire doesn't have a signal yet
        """
        if self.has_signal(left_input, right_input):
            operands = []
            for input_value in [left_input, right_input]:
                if isinstance(input_value, int) or input_value.isnumeric():
                    operands.append(int(input_value))
                else:
                    operands.append(self.wire_signals[input_value])
            return operands[0] & operands[1]
        else:
            raise ValueError("no signal for wire")

    def OR(self, left_input, right_input):
        """
        Perform bitwise OR operation on two inputs.

        Args:
            left_input: Wire name or numeric string
            right_input: Wire name or numeric string

        Returns:
            int: Bitwise OR result

        Raises:
            ValueError: If either input wire doesn't have a signal yet
        """
        if self.has_signal(left_input, right_input):
            operands = []
            for input_value in [left_input, right_input]:
                if input_value.isnumeric():
                    operands.append(int(input_value))
                else:
                    operands.append(self.wire_signals[input_value])
            return operands[0] | operands[1]
        else:
            raise ValueError("no signal for wire")

    def LSHIFT(self, wire_input, shift_amount):
        """
        Perform left shift operation on a wire signal.

        Args:
            wire_input: Wire name or numeric string to shift
            shift_amount: Number of positions to shift left

        Returns:
            int: Left-shifted result

        Raises:
            ValueError: If the input wire doesn't have a signal yet
        """
        if self.has_signal(wire_input, shift_amount):
            operands = []
            for input_value in [wire_input, shift_amount]:
                if input_value.isnumeric():
                    operands.append(int(input_value))
                else:
                    operands.append(self.wire_signals[input_value])
            return operands[0] << operands[1]
        else:
            raise ValueError("no signal for wire")

    def RSHIFT(self, wire_input, shift_amount):
        """
        Perform right shift operation on a wire signal.

        Args:
            wire_input: Wire name or numeric string to shift
            shift_amount: Number of positions to shift right

        Returns:
            int: Right-shifted result

        Raises:
            ValueError: If the input wire doesn't have a signal yet
        """
        if self.has_signal(wire_input, shift_amount):
            operands = []
            for input_value in [wire_input, shift_amount]:
                if input_value.isnumeric():
                    operands.append(int(input_value))
                else:
                    operands.append(self.wire_signals[input_value])
            return operands[0] >> operands[1]
        else:
            raise ValueError("no signal for wire")

    def NOT(self, wire_input):
        """
        Perform bitwise NOT (complement) operation on a wire signal.

        Args:
            wire_input: Wire name or numeric string to complement

        Returns:
            int: Bitwise complement result

        Raises:
            ValueError: If the input wire doesn't have a signal yet
        """
        if self.has_signal(wire_input):
            return ~int(wire_input)
        else:
            raise ValueError("no signal for wire")

    def _process_direct_assignment(self, source_part, dest_wire):
        """Helper method to process direct assignment instructions."""
        if not self.has_signal(source_part):
            return False
        if source_part.isnumeric():
            self.wire_signals[dest_wire] = int(source_part)
        else:
            self.wire_signals[dest_wire] = self.wire_signals[source_part]
        return True

    def _process_not_operation(self, source_wire, dest_wire):
        """Helper method to process NOT operation instructions."""
        if not self.has_signal(source_wire):
            return False
        self.wire_signals[dest_wire] = self.NOT(self.wire_signals[source_wire])
        return True

    def _process_binary_operation(self, left_input, operation, right_input, dest_wire):
        """Helper method to process binary operation instructions."""
        if not self.has_signal(left_input, right_input):
            return False
        # Dynamically call the appropriate gate method
        self.wire_signals[dest_wire] = getattr(self, operation)(left_input, right_input)
        return True

    def process_instruction(self, instruction):
        """
        Process a single wire instruction and update the circuit state.

        Instructions can be:
        - Direct assignment: "123 -> x" or "x -> y"
        - Unary operation: "NOT x -> h"
        - Binary operation: "x AND y -> z", "x OR y -> e", "x LSHIFT 2 -> f", "y RSHIFT 2 -> g"

        Args:
            instruction: String describing the wire connection

        Returns:
            bool: True if instruction was successfully processed, False if dependencies not ready
        """
        # Parse instruction into source expression and destination wire
        source_expr, dest_wire = instruction.split(" -> ")
        source_parts = source_expr.split()

        try:
            # Case 1: Direct assignment (numeric value or wire copy)
            if len(source_parts) == 1:
                return self._process_direct_assignment(source_parts[0], dest_wire)

            # Case 2: Unary NOT operation
            elif len(source_parts) == 2:
                return self._process_not_operation(source_parts[1], dest_wire)

            # Case 3: Binary operations (AND, OR, LSHIFT, RSHIFT)
            else:
                left_input, gate_operation, right_input = source_parts
                return self._process_binary_operation(left_input, gate_operation, right_input, dest_wire)

        except ValueError:
            return False


def solve_part2():
    """
    Simulate the circuit twice for Part 2.

    First run: Process all instructions to get the signal on wire 'a'.
    Second run: Reset the circuit, override wire 'b' with the value from wire 'a',
                then re-run the circuit while skipping any instruction that would
                assign to wire 'b' (to preserve the override).

    Part 2 instruction: "Take the signal you got on wire a, override wire b to that
    signal, and reset the other wires (including wire a)."

    Returns:
        int: The new signal value on wire 'a' after the override
    """
    lines = AoCInput.read_lines(INPUT_FILE)

    # First run: Get the initial signal on wire 'a'
    circuit = Circuit()
    pending_instructions = [line.strip() for line in lines]

    while pending_instructions:
        deferred_instructions = []
        for instruction in pending_instructions:
            if not circuit.process_instruction(instruction):
                deferred_instructions.append(instruction)
        pending_instructions = deferred_instructions[:]

    # Save the signal from wire 'a'
    signal_from_a = circuit.wire_signals["a"]

    # Second run: Reset circuit and override wire 'b'
    circuit = Circuit()
    circuit.wire_signals["b"] = signal_from_a

    # Re-process instructions, but skip any that assign to wire 'b'
    pending_instructions = [line.strip() for line in lines]
    # Filter out any instruction that assigns to wire 'b'
    pending_instructions = [inst for inst in pending_instructions if not inst.endswith(" -> b")]

    while pending_instructions:
        deferred_instructions = []
        for instruction in pending_instructions:
            if not circuit.process_instruction(instruction):
                deferred_instructions.append(instruction)
        pending_instructions = deferred_instructions[:]

    # Return the new signal on wire 'a'
    return circuit.wire_signals["a"]


answer = solve_part2()
AoCUtils.print_solution(2, answer)
