"""
Advent of Code 2017 - Day 22: Sporifica Virus (Part 2)

In Part 2, the virus evolves to have four states instead of two:
- Clean (0 or not in dictionary)
- Weakened (1)
- Infected (2)
- Flagged (3)

The carrier's behavior changes each burst:
1. Clean node: turn left, become weakened
2. Weakened node: no turn, become infected (counts as an infection)
3. Infected node: turn right, become flagged
4. Flagged node: reverse direction, become clean

After 10, 000, 000 bursts, count how many times a node becomes infected.
"""
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/22/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402


class EvolvedVirusCarrier():
    """Simulates an evolved virus carrier with 4-state nodes."""
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

    def burst(self, node_states):
        """Perform one burst of activity with evolved virus rules.

        Node states: 0=clean, 1=weakened, 2=infected, 3=flagged

        Args:
            node_states: Dictionary mapping positions to state values
        """
        # Determine current node state and act accordingly
        if self.location in node_states:
            state = node_states[self.location]
            if state == 2:
                # Infected: turn right
                self.turn_right()
            elif state == 3:
                # Flagged: reverse direction
                self.turn_right()
                self.turn_right()
        else:
            # Clean: turn left
            self.turn_left()

        # Transition node to next state
        if self.location in node_states:
            if node_states[self.location] == 3:
                # Flagged -> Clean (remove from dictionary)
                del node_states[self.location]
            elif node_states[self.location] == 2:
                # Infected -> Flagged
                node_states[self.location] += 1
            elif node_states[self.location] == 1:
                # Weakened -> Infected (this counts as an infection!)
                node_states[self.location] += 1
                self.infection_count += 1
        else:
            # Clean -> Weakened
            node_states[self.location] = 1

        # Move forward
        self.move_forward()


def main():
    """Simulate evolved virus spread for 10, 000, 000 bursts and count infections."""
    lines = AoCInput.read_lines(INPUT_FILE)

    # Parse the initial grid - infected nodes start at state 2
    node_states = {}
    max_x = 0
    max_y = 0
    for y, line in enumerate(lines):
        max_y = max(y, max_y)
        for x, node in enumerate(line):
            max_x = max(x, max_x)
            if node == '#':
                node_states[(x, y)] = 2

    # Initialize virus carrier at center of grid
    virus = EvolvedVirusCarrier()
    virus.location = (int(max_x/2), int(max_y/2))

    # Run 10,000,000 bursts
    for _ in range(10000000):
        virus.burst(node_states)

    AoCUtils.print_solution(2, virus.infection_count)


if __name__ == "__main__":
    main()
