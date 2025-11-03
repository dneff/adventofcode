"""
Advent of Code 2017 - Day 16: Permutation Promenade (Part 2)

The dance is performed one billion times! Simulating all iterations would be too slow.

The key insight: The dance moves create a cycle. After some number of iterations, the
programs return to their starting positions. By detecting this cycle, we can calculate
which state in the cycle corresponds to the billionth iteration without actually
performing all billion dances.

Strategy:
1. Perform the dance repeatedly
2. Track when we return to the starting configuration
3. Calculate the cycle length
4. Use modulo arithmetic to find the state at iteration 1,000,000,000
"""

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/16/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


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
            spin_count = int(instruction[1:])
            self.spin(spin_count)
        elif move_type == 'x':
            pos_a, pos_b = [int(x) for x in instruction[1:].split('/')]
            self.exchange(pos_a, pos_b)
        elif move_type == 'p':
            name_a, name_b = instruction[1:].split('/')
            self.partner(name_a, name_b)

    def spin(self, count):
        """Rotate programs: move count programs from end to front."""
        self.programs = self.programs[-count:] + self.programs[:-count]

    def exchange(self, pos_a, pos_b):
        """Swap programs at two positions."""
        self.programs[pos_a], self.programs[pos_b] = self.programs[pos_b], self.programs[pos_a]

    def partner(self, name_a, name_b):
        """Swap two programs by name."""
        idx_a = self.programs.index(name_a)
        idx_b = self.programs.index(name_b)
        self.programs[idx_a], self.programs[idx_b] = self.programs[idx_b], self.programs[idx_a]


def main():
    """Find program order after one billion dances using cycle detection."""
    line = AoCInput.read_lines(INPUT_FILE)[0]
    instructions = line.strip().split(',')

    simulator = DanceSimulator()
    simulator.instructions = instructions
    starting_configuration = simulator.programs[:]

    # Perform dance once first
    simulator.run()

    # Detect cycle: find when we return to starting configuration
    cycle_states = []
    target_iterations = 1000000000

    for cycle_num in range(1, target_iterations + 1):
        simulator.run()

        if simulator.programs == starting_configuration:
            cycle_states.append(cycle_num)

        # We've found enough cycles to determine the pattern
        if len(cycle_states) >= 3:
            break

    # Calculate cycle length
    cycle_length = cycle_states[-1] - cycle_states[-2]

    # Find how many additional iterations needed after the last complete cycle
    remaining_iterations = target_iterations - 1 - cycle_states[-1]
    remaining_iterations = remaining_iterations % cycle_length

    # Perform remaining dances
    for _ in range(remaining_iterations):
        simulator.run()

    final_order = ''.join(simulator.programs)
    AoCUtils.print_solution(2, final_order)


if __name__ == "__main__":
    main()
