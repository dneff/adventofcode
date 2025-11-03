"""
Advent of Code 2016 - Day 25: Clock Signal
https://adventofcode.com/2016/day/25

This solution finds the lowest positive integer to initialize register 'a' that causes
the assembunny code to output an alternating clock signal pattern: 0, 1, 0, 1, 0, 1...

The antenna on the roof requires this specific timing signal to properly read transmitted data.
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/25/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils

class BunnyPC():
    """
    Assembunny computer interpreter for generating clock signals.

    This interpreter extends the standard assembunny instruction set with an 'out' instruction
    that transmits values to create the clock signal pattern needed by the antenna.
    """
    def __init__(self):
        self.register = {"a":0, "b":0, "c":0, "d":0}  # Four registers for the assembunny computer
        self.code = []  # Assembunny program instructions
        self.signal = []  # Clock signal output values (produced by 'out' instruction)
        self.instruction_pointer = 0  # Current position in the program

    def load(self, filename):
        """Load assembunny program from input file."""
        lines = AoCInput.read_lines(filename)
        for line in lines:
            self.code.append(line.strip())

    def clear(self):
        """Reset the computer state for testing a new initial value."""
        self.register = {"a":0, "b":0, "c":0, "d":0}
        self.instruction_pointer = 0
        self.signal.clear()  # Clear previous clock signal output

    def resolveX(self, x):
        """Resolve parameter x to either a register value or integer literal."""
        if x in "abcd":
            return self.register[x]
        return int(x)

    def cpy(self, x, y):
        # cpy x y copies x (either an integer or the value of a register) into register y.
        self.register[y] = self.resolveX(x)
        self.instruction_pointer += 1

    def inc(self, x):
        # inc x increases the value of register x by one.
        self.register[x] += 1
        self.instruction_pointer += 1

    def dec(self, x):
        # dec x decreases the value of register x by one.
        self.register[x] -= 1
        self.instruction_pointer += 1

    def mul(self, x, y, z):
        # mul x y z stores the multiple of y and z in register x.
        self.register[x] += self.resolveX(y) * self.resolveX(z)
        self.instruction_pointer += 1

    def jnz(self, x, y):
        #jnz x y jumps to an instruction y away 
        # (positive means forward; negative means backward)
        # but only if x is not zero.
        if self.resolveX(x) != 0:
            self.instruction_pointer += self.resolveX(y)
        else:
            self.instruction_pointer += 1
    
    def tgl(self, x):
        # For one-argument instructions, inc becomes dec, and all other one-argument instructions become inc.
        # For two-argument instructions, jnz becomes cpy, and all other two-instructions become jnz.
        # The arguments of a toggled instruction are not affected.
        # If an attempt is made to toggle an instruction outside the program, nothing happens.
        # If toggling produces an invalid instruction (like cpy 1 2) and an attempt is later made to execute that instruction, skip it instead.
        # If tgl toggles itself (for example, if a is 0, tgl a would target itself and become inc a), the resulting instruction is not executed until the next time it is reached.
        toggle_pointer = self.instruction_pointer + self.register[x]
        if toggle_pointer < 0 or toggle_pointer > (len(self.code) - 1):
            self.instruction_pointer += 1
            return
        toggle_inst = self.code[toggle_pointer].split()
        if len(toggle_inst) == 2:
            if toggle_inst[0] == 'inc':
                toggle_inst[0] = 'dec'
            else:
                toggle_inst[0] = 'inc'
        elif len(toggle_inst) == 3:
            if toggle_inst[0] == 'jnz':
                toggle_inst[0] = 'cpy'
            else:
                toggle_inst[0] = 'jnz'
        self.code[toggle_pointer] = ' '.join(toggle_inst)
        #print(self.code[toggle_pointer], toggle_inst)
        self.instruction_pointer += 1           


    def run(self):
        while self.instruction_pointer < len(self.code):
            inst = self.code[self.instruction_pointer].split()
            command = getattr(self, inst[0])
            command(*inst[1:])

    def step(self):
        if self.instruction_pointer < len(self.code):
            inst = self.code[self.instruction_pointer].split()
            command = getattr(self, inst[0])
            command(*inst[1:])

    def out(self, x):
        """
        Output instruction (Day 25 specific): Transmit value x to the clock signal.

        This is the key instruction for this problem - it outputs values that form
        the clock signal pattern. We need the pattern to be: 0, 1, 0, 1, 0, 1...
        """
        self.signal.append(self.resolveX(x))
        self.instruction_pointer += 1

def main():
    """
    Find the lowest positive integer that produces a valid clock signal.

    Strategy:
    1. Test each initial value for register 'a' starting from 0
    2. Run the assembunny program and capture the clock signal output
    3. Check if the output matches the expected alternating pattern: 0,1,0,1,0,1...
    4. Return the first value that produces the correct pattern
    """

    initial_a_value = 0  # Initial value to test in register 'a'
    expected_clock_signal = [0,1] * 5  # Expected alternating clock signal pattern (checking first 10 outputs)

    # Initialize the assembunny computer (antenna's signal generator)
    antenna_computer = BunnyPC()
    antenna_computer.register['a'] = initial_a_value
    antenna_computer.load(INPUT_FILE)

    searching = True  # Flag to continue searching for the correct initial value

    # Search for the correct initial value that produces a valid clock signal
    while searching:
        # Run the program until we have enough clock signal output to test
        while len(antenna_computer.signal) < len(expected_clock_signal):
            antenna_computer.step()

        # Check if the clock signal matches the expected alternating pattern
        if antenna_computer.signal == expected_clock_signal:
            searching = False  # Found the correct initial value!
        else:
            # Try the next value
            initial_a_value += 1
            antenna_computer.clear()  # Reset the computer state
            antenna_computer.register['a'] = initial_a_value  # Set new test value

    AoCUtils.print_solution(1, initial_a_value)


    


if __name__ == "__main__":
    main()
