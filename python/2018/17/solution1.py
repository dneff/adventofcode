"""
Advent of Code 2018 - Day 17: Reservoir Research (Part 1)
https://adventofcode.com/2018/day/17

Water flows from a spring at coordinates (500, 0) through a landscape of sand and clay.
This solution simulates water movement where it flows downward when possible and spreads
horizontally when blocked by clay, determining how many tiles the water can reach.
"""
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2018/17/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))
from aoc_helpers import AoCUtils


class Scan():
    """Simulates water flow through a clay-and-sand landscape."""

    def __init__(self):
        self.clay = {}  # Clay positions
        self.water = {}  # Water positions with flow state ('|' or '~')
        self.previous_downs = []
        self.actions = []  # Queue of pending water flow actions
        self.seen = set()  # Track processed actions
        self.drip = (500, 0)  # Water source position
        self.x_min, self.x_max = 0, 0
        self.y_min, self.y_max = 0, 0
        self.add_action(self.drip, 'down')

    def flow_down(self, position):
        """
        Find all positions straight down until hitting clay or bottom.
        Mark them as flowing water ('|').
        """
        # Find blockers (clay or settled water) below this position
        blocker_clay = [x for x in self.clay if (x[0] == position[0] and x[1] > position[1])]
        blocker_water = [x for x in self.water if (x[0] == position[0] and x[1] > position[1])]
        blocker = blocker_clay[:] + blocker_water[:]
        if len(blocker) == 0:
            end = self.y_max + 1
        else:
            end = min([x[1] for x in blocker])

        # Queue horizontal flow if we hit a blocker
        if (position[0], end) in blocker_water:
            self.add_action((position[0], end), 'across')
        elif (position[0], end) in blocker_clay:
            self.add_action((position[0], end-1), 'across')

        # Mark all positions as flowing water
        for y in range(position[1], end):
            self.water[(position[0], y)] = '|'


    def flow_across(self, position):
        """
        Flow horizontally from this position until either:
        1. hitting water/clay
        2. not having water/clay underneath
        Marks water as settled ('~') if bounded, flowing ('|') otherwise.
        """
        # Mark current position as settled water
        self.water[position] = '~'
        if position[1] == self.y_max:
            return

        right_bounded = True
        left_bounded = True

        # Flow to the right
        x, y = position
        flowing_right = True
        seen_clay = (x, y+1) in self.clay
        while flowing_right:
            x += 1
            over_water = (x, y+1) in self.water and self.water[(x, y+1)] == '~'
            over_clay = (x, y+1) in self.clay
            seen_clay = over_clay or seen_clay
            flowing_right = (over_clay or over_water) and (x, y) not in self.clay and x <= self.x_max
            if flowing_right:
                self.water[(x, y)] = '~'
            else:
                if (x, y) not in self.clay:
                    self.add_action((x, y), 'down')
                    right_bounded = False

        # Flow to the left
        x, y = position
        flowing_left = True
        seen_clay = (x, y+1) in self.clay
        while flowing_left:
            x -= 1
            over_water = (x, y+1) in self.water and self.water[(x, y+1)] == '~'
            over_clay = (x, y+1) in self.clay
            seen_clay = over_clay or seen_clay
            flowing_left = (over_clay or over_water) and (x, y) not in self.clay and x >= self.x_min
            if flowing_left:
                self.water[(x, y)] = '~'
            else:
                if (x, y) not in self.clay:
                    self.add_action((x, y), 'down')
                    left_bounded = False

        # If water is bounded on both sides, propagate upward
        if right_bounded and left_bounded:
            self.add_action((position[0], position[1] - 1), 'across')


    def add_action(self, position, direction):
        """Add a water flow action to the queue if not already seen."""
        if direction in ['down', 'across']:
            action = ((position), direction)
            if action not in self.seen:
                self.seen.add(action)
                self.actions.append(((position), direction))
        else:
            raise ValueError(f"Not a valid direction: {direction}")


    def process_action(self):
        """Process the next water flow action from the queue."""
        if len(self.actions) == 0:
            return False
        position, direction = self.actions.pop(0)
        if direction == 'across':
            self.flow_across(position)
        elif direction == 'down':
            self.flow_down(position)
        else:
            raise ValueError(f"direction is invalid: {direction}")
        return True

    def __repr__(self):
        """Generate a visual representation of the scan for debugging."""
        output = []
        for y in range(self.y_min - 1, self.y_max + 2):
            row = ''
            for x in range(self.x_min - 1, self.x_max + 1):
                if (x, y) in self.clay and (x, y) in self.water:
                    row = row + '&'
                elif (x, y) in self.clay:
                    row = row + self.clay[(x, y)]
                elif (x, y) in self.water:
                    row = row + self.water[(x, y)]
                else:
                    row = row + ' '
            output.append(row)
        return '\n'.join(output[0:100])


def main():
    """Simulate water flow and count reachable tiles."""
    file = open(INPUT_FILE, 'r', encoding='utf-8')

    scan = Scan()

    # Parse clay positions from input
    for line in file.readlines():
        part_a, part_b = line.strip().split(', ')
        a = int(part_a.split('=')[-1])
        b_min, b_max = [int(x) for x in part_b.split('=')[-1].split('..')]
        for b in range(b_min, b_max + 1):
            if part_a[0] == 'x':
                scan.clay[(a, b)] = '#'
            else:
                scan.clay[(b, a)] = '#'

    # Calculate scan boundaries
    x_all = [x[0] for x in scan.clay]
    y_all = [x[1] for x in scan.clay]
    scan.x_min, scan.x_max = min(x_all), max(x_all)
    scan.y_min, scan.y_max = min(y_all), max(y_all)

    # Process all water flow actions
    cycles = 0
    while scan.process_action():
        cycles += 1

    # Count water tiles within the vertical bounds
    valid_water = [w for w in scan.water.keys() if w[1] >= scan.y_min]
    AoCUtils.print_solution(1, len(valid_water))


if __name__ == "__main__":
    main()
