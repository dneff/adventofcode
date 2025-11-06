"""
Advent of Code 2017 - Day 25: The Halting Problem (Part 1)

Implement a Turing machine based on blueprints to determine its diagnostic checksum.

A Turing machine has:
- An infinite tape containing 0s and 1s
- A cursor that reads/writes values and moves left or right
- Multiple states with rules defining behavior based on current tape values

After running the machine for a specified number of steps (12, 425, 180 for this input),
count how many 1s appear on the tape. This count is the diagnostic checksum.

Note: The state machine logic is hardcoded based on the puzzle input blueprints.
"""
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/25/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCUtils  # noqa: E402
from collections import defaultdict  # noqa: E402


class TuringMachine():
    """Simulates a Turing machine with configurable state transitions."""
    def __init__(self):
        self.cycles = 0
        self.state = getattr(self, 'state_a')  # Start in state A
        self.tape = defaultdict(int)  # Infinite tape, defaults to 0
        self.cursor = 0  # Current position on tape

    def run(self, cycles):
        """Execute the Turing machine for a specified number of cycles.

        Args:
            cycles: Number of steps to execute
        """
        self.cycles = cycles
        while self.cycles > 0:
            self.state()
            self.cycles -= 1
            # Progress indicator for long runs
            if self.cycles % 100000 == 0:
                print(f"{self.cycles}/{cycles}")

    def checksum(self):
        """Calculate the diagnostic checksum (count of 1s on the tape).

        Returns:
            Number of tape positions containing 1
        """
        return sum(self.tape.values())

    def state_a(self):
        """State A transition rules (specific to puzzle input)."""
        if self.tape[self.cursor] == 0:
            self.tape[self.cursor] = 1
            self.cursor += 1
            self.state = getattr(self, 'state_b')
        else:
            self.tape[self.cursor] = 0
            self.cursor += 1
            self.state = getattr(self, 'state_f')

    def state_b(self):
        """State B transition rules (specific to puzzle input)."""
        if self.tape[self.cursor] == 0:
            self.tape[self.cursor] = 0
            self.cursor -= 1
            self.state = getattr(self, 'state_b')
        else:
            self.tape[self.cursor] = 1
            self.cursor -= 1
            self.state = getattr(self, 'state_c')

    def state_c(self):
        """State C transition rules (specific to puzzle input)."""
        if self.tape[self.cursor] == 0:
            self.tape[self.cursor] = 1
            self.cursor -= 1
            self.state = getattr(self, 'state_d')
        else:
            self.tape[self.cursor] = 0
            self.cursor += 1
            self.state = getattr(self, 'state_c')

    def state_d(self):
        """State D transition rules (specific to puzzle input)."""
        if self.tape[self.cursor] == 0:
            self.tape[self.cursor] = 1
            self.cursor -= 1
            self.state = getattr(self, 'state_e')
        else:
            self.tape[self.cursor] = 1
            self.cursor += 1
            self.state = getattr(self, 'state_a')

    def state_e(self):
        """State E transition rules (specific to puzzle input)."""
        if self.tape[self.cursor] == 0:
            self.tape[self.cursor] = 1
            self.cursor -= 1
            self.state = getattr(self, 'state_f')
        else:
            self.tape[self.cursor] = 0
            self.cursor -= 1
            self.state = getattr(self, 'state_d')

    def state_f(self):
        """State F transition rules (specific to puzzle input)."""
        if self.tape[self.cursor] == 0:
            self.tape[self.cursor] = 1
            self.cursor += 1
            self.state = getattr(self, 'state_a')
        else:
            self.tape[self.cursor] = 0
            self.cursor -= 1
            self.state = getattr(self, 'state_e')

    def __str__(self):
        """Return a string representation of the tape contents."""
        tape_positions = list(self.tape.keys())
        tape_positions.sort()
        return f"{[self.tape[pos] for pos in tape_positions]}"


def main():
    """Run the Turing machine and calculate the diagnostic checksum."""
    machine = TuringMachine()
    machine.run(12425180)

    AoCUtils.print_solution(1, machine.checksum())


if __name__ == "__main__":
    main()
