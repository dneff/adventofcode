"""
Advent of Code 2017 - Day 18: Duet (Part 1)

You discover a tablet with assembly-like instructions. The goal is to execute
the program and find the value of the recovered frequency the first time a
'rcv' instruction is executed with a non-zero value.

Instructions:
- snd X: plays a sound with frequency equal to X's value
- set X Y: sets register X to Y's value
- add X Y: increases register X by Y's value
- mul X Y: multiplies register X by Y's value
- mod X Y: sets X to the remainder of X divided by Y
- rcv X: recovers the last sound's frequency (only if X is non-zero)
- jgz X Y: jumps by Y's offset if X is greater than zero
"""
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/18/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402
from collections import defaultdict  # noqa: E402
from string import ascii_lowercase as letters  # noqa: E402


class DuetProgram():
    """Simulates a single-threaded assembly program that plays sounds."""
    def __init__(self):
        self.program = []
        self.last_sound_played = 0  # Frequency of the most recently played sound
        self.pointer = 0  # Instruction pointer
        self.registers = defaultdict(int)

    def run(self):
        """Execute the program instructions until completion.

        Runs instructions sequentially, advancing the instruction pointer
        until it goes out of range of the instruction list.
        """
        while -1 < self.pointer < len(self.program):
            instruction = self.program[self.pointer]
            i = getattr(self, instruction[0])
            i(*instruction[1:],)
            if instruction[0] != 'jgz':
                self.pointer += 1

    def snd(self, x):
        """Play a sound with a frequency equal to the value of X.

        Args:
            x: Register name containing the frequency value
        """
        self.last_sound_played = self.registers[x]

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
        """Recover the frequency of the last sound played (only if X is non-zero).

        If the value in register X is not zero, recovers the last sound frequency.
        When a non-zero frequency is recovered, prints the solution and exits.

        Args:
            x: Register name to check for non-zero value
        """
        if self.registers[x] != 0:
            self.registers[x] = self.last_sound_played
            if self.last_sound_played != 0:
                AoCUtils.print_solution(1, self.last_sound_played)
                exit(0)

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
    """Parse and execute the Duet assembly program to find the recovered frequency."""
    program = DuetProgram()
    lines = AoCInput.read_lines(INPUT_FILE)
    for line in lines:
        program.program.append(line.strip().split())

    program.run()


if __name__ == "__main__":
    main()
