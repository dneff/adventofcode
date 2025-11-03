"""
Advent of Code 2017 - Day 18: Duet (Part 2)

In Part 2, the program interpretation changes completely. Now 'snd' sends values
to another program and 'rcv' receives from a buffer. Two programs run in parallel,
each with their own set of registers and a unique program ID (0 and 1) in register 'p'.

The programs communicate via message queues. When a program tries to receive but
has no messages, it waits. When both programs are waiting (deadlock), execution stops.

The goal is to determine how many times program 1 sends a value.
"""
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/18/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
from collections import defaultdict
from string import ascii_lowercase as letters


class DuetProgram():
    """Simulates a concurrent program that communicates with another program via message passing."""
    def __init__(self, program_id):
        self.id = program_id
        self.partner_program = None  # Reference to the other program
        self.program = []
        self.receive_buffer = []  # Incoming messages queue
        self.send_count = 0  # Number of values sent to partner
        self.pointer = 0  # Instruction pointer
        self.waiting = False  # True when blocked waiting for input
        self.registers = defaultdict(int)

    def run(self):
        """Execute instructions until blocked or program terminates.

        Runs instructions sequentially until:
        - The instruction pointer goes out of range (program terminates)
        - A receive instruction blocks due to empty buffer (waiting state)
        """
        while -1 < self.pointer < len(self.program):
            instruction = self.program[self.pointer]
            i = getattr(self, instruction[0])
            i(*instruction[1:],)
            if instruction[0] != 'jgz':
                self.pointer += 1
            # If blocked on receive, return control to allow partner to run
            if self.waiting == True:
                return
        # Program terminated (pointer out of range)
        self.waiting = True
        return

    def snd(self, x):
        """Send a value to the partner program's receive buffer.

        Args:
            x: Register name or literal value to send
        """
        self.partner_program.receive_buffer.append(str(self.get(x)))
        self.send_count += 1

    def set(self, x, y):
        """sets register X to the value of Y"""
        self.registers[x] = self.get(y)

    def add(self, x, y):
        """increases register X by the value of Y"""
        self.registers[x] += self.get(y)

    def mul(self, x, y):
        """sets register X to the result of multiplying
        the value contained in register X by the value of Y"""
        self.registers[x] *= self.get(y)

    def mod(self, x, y):
        """sets register X to the remainder of dividing
        the value contained in register X by the value
        of Y (that is, it sets X to the result of X modulo Y)"""
        self.registers[x] %= self.get(y)

    def rcv(self, x):
        """Receive a value from the buffer and write to register X.

        If the buffer is empty, the program waits (blocks) and backs up
        the instruction pointer to retry this instruction later.

        Args:
            x: Register name to store the received value
        """
        if len(self.receive_buffer) > 0:
            self.waiting = False
            self.registers[x] = self.get(self.receive_buffer.pop(0))
            return
        else:
            # Block: set waiting flag and rewind pointer to retry this instruction
            self.waiting = True
            self.pointer -= 1

    def jgz(self, x, y):
        """jumps with an offset of the value of Y,
        but only if the value of X is greater than zero.
        (An offset of 2 skips the next instruction, an
        offset of -1 jumps to the previous instruction, and so on.)"""

        if self.get(x) > 0:
            self.pointer += self.get(y)
        else:
            self.pointer += 1

    def get(self, x):
        """Get the value of x, either from a register or as a literal integer.

        Args:
            x: Either a register name (letter) or a string representation of an integer

        Returns:
            The integer value from the register or the literal value
        """
        if x in letters:
            return self.registers[x]
        else:
            return int(x)


def main():
    """Run two Duet programs in parallel and count how many times program 1 sends values."""
    # Create two programs with IDs 0 and 1
    program0 = DuetProgram(0)
    program0.registers['p'] = 0
    program1 = DuetProgram(1)
    program1.registers['p'] = 1

    # Link the programs so they can communicate
    program0.partner_program = program1
    program1.partner_program = program0

    # Load the same program into both
    lines = AoCInput.read_lines(INPUT_FILE)
    for line in lines:
        program0.program.append(line.strip().split())
        program1.program.append(line.strip().split())

    # Run both programs until both are waiting (deadlock) with no messages in transit
    while (not program0.waiting or not program1.waiting or
           len(program0.receive_buffer) > 0 or len(program1.receive_buffer) > 0):
        program0.run()
        program1.run()

    AoCUtils.print_solution(2, program1.send_count)


if __name__ == "__main__":
    main()
