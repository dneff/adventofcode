import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2017/22/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


class GridBug():
    """simulated virus"""
    def __init__(self):
        self.next = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        self.heading = 0
        self.location = (0, 0)
        self.infection_count = 0

    def left(self):
        self.heading = (self.heading - 1) % 4

    def right(self):
        self.heading = (self.heading + 1) % 4

    def move(self):
        x, y = [a+b for a, b in zip(self.location, self.next[self.heading])]
        self.location = (x, y)

    def burst(self, node_status):
        if self.location in node_status:
            state = node_status[self.location]
            if state == 2:
                self.right()
            elif state == 3:
                self.right()
                self.right()
        else:
            self.left()

        if self.location in node_status:
            if node_status[self.location] == 3:
                del node_status[self.location]
            elif node_status[self.location] == 2:
                node_status[self.location] += 1
            elif node_status[self.location] == 1:
                node_status[self.location] += 1
                self.infection_count += 1
        else:
            node_status[self.location] = 1
        self.move()


def main():
    lines = AoCInput.read_lines(INPUT_FILE)

    node_status = {}

    max_x = 0
    max_y = 0
    for y, line in enumerate(lines):
        max_y = max(y, max_y)
        for x, node in enumerate(line):
            max_x = max(x, max_x)
            if node == '#':
                node_status[(x, y)] = 2

    virus = GridBug()
    virus.location = (int(max_x/2), int(max_y/2))

    for _ in range(10000000):
        virus.burst(node_status)

    AoCUtils.print_solution(2, virus.infection_count)


if __name__ == "__main__":
    main()
