"""
Advent of Code 2017 - Day 16: Permutation Promenade (Part 1)

Simulate a dance of 16 programs (labeled a-p) performing three types of moves:

1. Spin (sX): Move X programs from end to front, maintaining their order
   Example: s3 on 'abcde' produces 'cdeab'

2. Exchange (xA/B): Swap programs at positions A and B
   Example: x3/4 on 'eabcd' produces 'eabdc'

3. Partner (pA/B): Swap programs named A and B (regardless of position)
   Example: pe/b on 'eabdc' produces 'baedc'

Part 1: Determine the order of programs after one complete dance.
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/16/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402


class DanceSimulator():
    """Simulates the dancing programs and their three types of moves."""

    def __init__(self, num_programs=16):
        """
        Initialize with programs labeled a through p.

        Args:
            num_programs: Number of programs (default 16 for a-p)
        """
        self.programs = list('abcdefghijklmnop'[:num_programs])
        self.instructions = []

    def run(self):
        """Execute all dance instructions in sequence."""
        for instruction in self.instructions:
            self.execute_move(instruction)

    def execute_move(self, instruction):
        """
        Execute a single dance move.

        Args:
            instruction: String starting with 's', 'x', or 'p'
        """
        move_type = instruction[0]

        if move_type == 's':
            # Spin: move X programs from end to front
            spin_count = int(instruction[1:])
            self.spin(spin_count)
        elif move_type == 'x':
            # Exchange: swap positions
            pos_a, pos_b = [int(x) for x in instruction[1:].split('/')]
            self.exchange(pos_a, pos_b)
        elif move_type == 'p':
            # Partner: swap named programs
            name_a, name_b = instruction[1:].split('/')
            self.partner(name_a, name_b)

    def spin(self, count):
        """
        Rotate programs: move count programs from end to front.

        Args:
            count: Number of programs to move
        """
        self.programs = self.programs[-count:] + self.programs[:-count]

    def exchange(self, pos_a, pos_b):
        """
        Swap programs at two positions.

        Args:
            pos_a: First position
            pos_b: Second position
        """
        self.programs[pos_a], self.programs[pos_b] = self.programs[pos_b], self.programs[pos_a]

    def partner(self, name_a, name_b):
        """
        Swap two programs by name.

        Args:
            name_a: Name of first program
            name_b: Name of second program
        """
        idx_a = self.programs.index(name_a)
        idx_b = self.programs.index(name_b)
        self.programs[idx_a], self.programs[idx_b] = self.programs[idx_b], self.programs[idx_a]


def main():
    """Simulate the dance and print the final program order."""
    line = AoCInput.read_lines(INPUT_FILE)[0]
    instructions = line.strip().split(',')

    simulator = DanceSimulator()
    simulator.instructions = instructions
    simulator.run()

    final_order = ''.join(simulator.programs)
    AoCUtils.print_solution(1, final_order)


if __name__ == "__main__":
    main()
