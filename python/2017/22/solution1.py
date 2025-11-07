"""
Advent of Code 2017 - Day 22: Sporifica Virus (Part 1)

A virus carrier moves through an infinite 2D grid. Nodes can be clean or infected.
The carrier follows these rules in each burst:
1. If the current node is infected, turn right; otherwise turn left
2. Toggle the node's state (clean->infected, infected->clean)
3. Move forward one node in the current direction

Starting at the grid's center facing up, after 10, 000 bursts of activity,
count how many bursts cause a node to become infected.
"""
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/22/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402
from collections import defaultdict  # noqa: E402


class VirusCarrier():
    """Simulates a virus carrier moving through a 2D grid."""
    def __init__(self):
        self.directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # up, right, down, left
        self.heading = 0  # Start facing up
        self.location = (0, 0)
        self.infection_count = 0

    def turn_left(self):
        """Turn 90 degrees counter-clockwise."""
        self.heading = (self.heading - 1) % 4

    def turn_right(self):
        """Turn 90 degrees clockwise."""
        self.heading = (self.heading + 1) % 4

    def move_forward(self):
        """Move one step in the current direction."""
        x, y = [a+b for a, b in zip(self.location, self.directions[self.heading])]
        self.location = (x, y)

    def burst(self, infected_nodes):
        """Perform one burst of activity.

        Args:
            infected_nodes: Dictionary tracking infected node positions
        """
        # Turn based on current node state
        if self.location in infected_nodes:
            self.turn_right()
        else:
            self.turn_left()

        # Toggle node state
        if self.location in infected_nodes:
            del infected_nodes[self.location]
        else:
            infected_nodes[self.location] += 1
            self.infection_count += 1

        # Move forward
        self.move_forward()


def main():
    """Simulate virus spread for 10, 000 bursts and count infections."""
    lines = AoCInput.read_lines(INPUT_FILE)

    # Parse the initial grid of infected nodes
    infected_nodes = defaultdict(int)
    max_x = 0
    max_y = 0
    for y, line in enumerate(lines):
        max_y = max(y, max_y)
        for x, node in enumerate(line):
            max_x = max(x, max_x)
            if node == '#':
                infected_nodes[(x, y)] += 1

    # Initialize virus carrier at center of grid
    virus = VirusCarrier()
    virus.location = (max_x//2, max_y//2)

    # Run 10,000 bursts
    for _ in range(10000):
        virus.burst(infected_nodes)

    AoCUtils.print_solution(1, virus.infection_count)


if __name__ == "__main__":
    main()
