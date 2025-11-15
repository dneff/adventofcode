"""
IntCode computer implementation for Advent of Code 2019

This module implements a virtual machine for the IntCode computer, which is used
throughout multiple Advent of Code 2019 challenges (days 2, 5, 7, 9, 11, 13, 15, 17, 19, 21).

The IntCode computer is a simple virtual machine with:
- Memory: An array of integers (with automatic expansion)
- Instruction pointer: Tracks the current instruction
- Relative base: Used for relative addressing mode
- Input/Output queues: For communication with external systems
- Parameter modes: Position (0), Immediate (1), and Relative (2)

Modified for day 21 challenges:
    - Updated debugging output for robot/hull visualization
"""

from collections import deque


class InputInterrupt(Exception):
    """Raised when the computer needs input but the input queue is empty."""
    pass


class OutputInterrupt(Exception):
    """Raised when the computer produces output (used for step-by-step execution)."""
    pass

class IntCode:
    """
    IntCode virtual machine implementation.

    The IntCode computer executes programs written in a simple assembly-like language
    with opcodes for arithmetic, I/O, jumps, and comparisons.
    """

    def __init__(self, program_code, *args):
        """
        Initialize the IntCode computer.

        Args:
            program_code: String containing comma-separated integers representing the program
            *args: Optional initial input values to populate the input queue
        """
        self.program_code = program_code  # Original program code (for reset)
        self.debugging = False  # Whether to print debug output
        self.complete = False  # Whether the program has halted (opcode 99)

        # Parse program and allocate memory (with extra space for dynamic allocation)
        self.memory = [int(x) for x in self.program_code.strip().split(',')] + [0] * 200000

        self.instruction_pointer = 0  # Current position in the program
        self.relative_base = 0  # Base offset for relative addressing mode

        # Input/output queues for communication
        self.input = deque()
        self.output = deque()

        # Pre-populate input queue if provided
        if args:
            self.input = args[:]

    def reset(self):
        """Reset the computer to its initial state (re-parse program and clear I/O)."""
        self.instruction_pointer = 0
        self.input.clear()
        self.output.clear()
        self.memory = [int(x) for x in self.program_code.strip().split(',')] + [0] * 200000

    def pop(self):
        """Remove and return the next value from the output queue."""
        return self.output.popleft()

    def push(self, value):
        """Add a value to the input queue."""
        self.input.append(value)

    def advance_instruction_pointer(self, offset):
        """Move the instruction pointer forward by the specified offset."""
        self.instruction_pointer += offset

    def get_operation(self, opcode):
        """
        Get the operation function and parameter count for a given opcode.

        Args:
            opcode: The operation code (1-9)

        Returns:
            Tuple of (operation_function, parameter_count)
        """
        # Map opcodes to their handler functions
        opcode_to_function = {
            1: self.opcode_add,           # Addition
            2: self.opcode_multiply,      # Multiplication
            3: self.opcode_input,         # Read from input queue
            4: self.opcode_output,        # Write to output queue
            5: self.opcode_jump_if_true,  # Jump if non-zero
            6: self.opcode_jump_if_false, # Jump if zero
            7: self.opcode_less_than,     # Compare less than
            8: self.opcode_equals,        # Compare equals
            9: self.opcode_adjust_relative_base  # Adjust relative base
        }

        # Number of parameters each opcode takes
        opcode_param_count = {
            1: 3,  # add: 2 inputs + 1 output
            2: 3,  # multiply: 2 inputs + 1 output
            3: 1,  # input: 1 output
            4: 1,  # output: 1 input
            5: 2,  # jump-if-true: 1 condition + 1 destination
            6: 2,  # jump-if-false: 1 condition + 1 destination
            7: 3,  # less than: 2 inputs + 1 output
            8: 3,  # equals: 2 inputs + 1 output
            9: 1   # adjust relative base: 1 input
        }
        return opcode_to_function[opcode], opcode_param_count[opcode]

    # Opcode implementations (instruction handlers)
    # Each handler receives resolved parameters and updates the instruction pointer

    def opcode_add(self, parameters):
        """Opcode 1: Add parameters[0] + parameters[1] and store in parameters[2]."""
        self.memory[parameters[2]] = parameters[0] + parameters[1]
        self.advance_instruction_pointer(len(parameters) + 1)

    def opcode_multiply(self, parameters):
        """Opcode 2: Multiply parameters[0] * parameters[1] and store in parameters[2]."""
        self.memory[parameters[2]] = parameters[0] * parameters[1]
        self.advance_instruction_pointer(len(parameters) + 1)

    def opcode_input(self, parameters):
        """Opcode 3: Read from input queue and store in parameters[0]."""
        try:
            self.memory[parameters[0]] = self.input.popleft()
        except IndexError:
            # No input available - raise interrupt so caller can provide input
            raise InputInterrupt
        else:
            self.advance_instruction_pointer(len(parameters) + 1)

    def opcode_output(self, parameters):
        """Opcode 4: Write parameters[0] to output queue."""
        value = parameters[0]
        self.output.append(value)

        # Debug output for springbot visualization (show ASCII or numeric values)
        if value < 128:
            # ASCII character output (hull visualization)
            self.debug(f"OUTPUT: {value:3d} ('{chr(value)}')")
        else:
            # Large numeric value (likely final damage report)
            self.debug(f"OUTPUT: {value} (DAMAGE VALUE)")

        self.advance_instruction_pointer(len(parameters) + 1)
        # Raise interrupt to allow step-by-step execution
        raise OutputInterrupt

    def opcode_jump_if_true(self, parameters):
        """Opcode 5: If parameters[0] is non-zero, jump to parameters[1]."""
        if parameters[0] != 0:
            self.instruction_pointer = parameters[1]
        else:
            self.advance_instruction_pointer(len(parameters) + 1)

    def opcode_jump_if_false(self, parameters):
        """Opcode 6: If parameters[0] is zero, jump to parameters[1]."""
        if parameters[0] == 0:
            self.instruction_pointer = parameters[1]
        else:
            self.advance_instruction_pointer(len(parameters) + 1)

    def opcode_less_than(self, parameters):
        """Opcode 7: Store 1 in parameters[2] if parameters[0] < parameters[1], else 0."""
        if parameters[0] < parameters[1]:
            self.memory[parameters[2]] = 1
        else:
            self.memory[parameters[2]] = 0
        self.advance_instruction_pointer(len(parameters) + 1)

    def opcode_equals(self, parameters):
        """Opcode 8: Store 1 in parameters[2] if parameters[0] == parameters[1], else 0."""
        if parameters[0] == parameters[1]:
            self.memory[parameters[2]] = 1
        else:
            self.memory[parameters[2]] = 0
        self.advance_instruction_pointer(len(parameters) + 1)

    def opcode_adjust_relative_base(self, parameters):
        """Opcode 9: Adjust the relative base by parameters[0]."""
        self.relative_base += parameters[0]
        self.advance_instruction_pointer(len(parameters) + 1)
    
    def parse_parameter_modes(self, mode_digits):
        """
        Parse parameter mode digits into a list of individual modes.

        Parameter modes determine how to interpret parameters:
        - Mode 0 (Position): Parameter is a memory address
        - Mode 1 (Immediate): Parameter is a literal value
        - Mode 2 (Relative): Parameter is an offset from the relative base

        Args:
            mode_digits: Integer representing mode digits (e.g., 1002 → [0, 1, 0])

        Returns:
            List of mode values, one per parameter (least significant digit first)
        """
        # Convert to string, pad to at least 3 digits, and reverse
        # Example: 1002 → "1002" → "002" (last 3 digits) → [2, 0, 0] → modes for params
        return [int(digit) for digit in str(mode_digits).zfill(3)[::-1]]

    def resolve_parameters(self, raw_parameters, mode_digits, opcode):
        """
        Resolve raw parameters based on their addressing modes.

        For input parameters (read), dereference the memory address.
        For output parameters (write), return the address itself.

        Args:
            raw_parameters: List of raw parameter values from memory
            mode_digits: Integer encoding the parameter modes
            opcode: The current opcode (affects parameter interpretation)

        Returns:
            List of resolved parameter values
        """
        resolved = raw_parameters[:]
        modes = self.parse_parameter_modes(mode_digits)

        for idx, mode in enumerate(modes[:len(raw_parameters)]):
            # Mode 0: Position mode - parameter is a memory address
            if mode == 0:
                if raw_parameters[idx] < 0:
                    raise Exception(f"Invalid memory location: {raw_parameters[idx]}")
                # For input/read parameters, dereference the address
                # For output/write parameters (3rd param of most ops, 1st param of input op), keep the address
                if opcode not in [3] and idx < 2:
                    resolved[idx] = self.memory[raw_parameters[idx]]
                else:
                    resolved[idx] = raw_parameters[idx]

            # Mode 1: Immediate mode - parameter is a literal value
            elif mode == 1:
                resolved[idx] = raw_parameters[idx]

            # Mode 2: Relative mode - parameter is offset from relative base
            elif mode == 2:
                # For read parameters, dereference the computed address
                # For write parameters, return the computed address
                if opcode not in [3] and idx < 2:
                    resolved[idx] = self.memory[raw_parameters[idx] + self.relative_base]
                else:
                    resolved[idx] = raw_parameters[idx] + self.relative_base

        return resolved

    def run(self):
        """
        Execute the IntCode program until it halts (opcode 99) or raises an interrupt.

        The execution loop:
        1. Read instruction at current position (opcode + mode digits)
        2. Parse opcode and parameter modes
        3. Extract and resolve parameters based on modes
        4. Execute the operation
        5. Repeat until halt or interrupt

        Raises:
            InputInterrupt: When input is needed but queue is empty
            OutputInterrupt: When output is produced (for step-by-step execution)
        """
        while not self.complete:
            # Decode instruction: last 2 digits are opcode, rest are parameter modes
            # Example: 1002 → modes=10, opcode=2 (multiply with mode 0, 1, 0)
            mode_digits, opcode = divmod(self.memory[self.instruction_pointer], 100)

            # Opcode 99 = halt
            if opcode == 99:
                self.complete = True
                break

            # Get the operation handler and parameter count for this opcode
            operation, param_count = self.get_operation(opcode)

            # Extract raw parameters from memory
            param_start = self.instruction_pointer + 1
            param_end = param_start + param_count
            raw_params = self.memory[param_start:param_end]

            # Resolve parameters based on their addressing modes
            resolved_params = self.resolve_parameters(raw_params, mode_digits, opcode)

            self.debug("---")

            # Execute the operation (may raise InputInterrupt or OutputInterrupt)
            operation(resolved_params)

    def debug(self, message):
        """Print debug message if debugging is enabled."""
        if self.debugging:
            print(message)
