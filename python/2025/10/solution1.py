"""
Advent of Code 2025 - Day 10: Factory
https://adventofcode.com/2025/day/10

The input describes one machine per line. Each line contains a single indicator 
light diagram in [square brackets], one or more button wiring schematics in 
(parentheses), and joltage requirements in {curly braces}.

Part 1

To start a machine, its indicator lights must match those shown in the diagram, 
where . means off and # means on. The machine has the number of indicator lights 
shown, but its indicator lights are all initially off.

You can toggle the state of indicator lights by pushing any of the listed 
buttons.

You have to push each button an integer number of times (possibly zero). Each 
time you push a button, it toggles the state of each of its connected indicator 
lights. If a button is connected to an indicator light that is currently off, it 
turns on; if it is connected to an indicator light that is currently on, it 
turns off.

Analyze each machine's indicator light diagram and button wiring schematics. What 
is the fewest button presses required to correctly configure the indicator lights 
on all of the machines?

Strategy:
For each machine, we can represent the indicator lights and button connections
as binary numbers. The target configuration is derived from the indicator light
diagram, and each button's effect is represented as a binary mask. We can use
bitwise operations to determine the minimum number of button presses needed to
achieve the target configuration.

This is a breadth-first search (BFS) problem in the space of button press
combinations. We will explore all possible configurations by pressing buttons and
track the minimum presses needed to reach the target configuration. We stop when a path
repeats or when we reach the target configuration.
"""

import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "../../"))

from aoc_helpers import AoCInput, AoCUtils, Pathfinding  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, "../../../../aoc-data/2025/10/input")
machines = AoCInput.read_lines(INPUT_FILE)

def parse_machine(line):
    """Parse a machine line into its components."""
    light_diagram = line[line.index('[')+1:line.index(']')]
    button_schematics = line[line.index('] (')+3:line.index(') {')].strip().split(') (')
    
    target_config = 0
    for i, light in enumerate(light_diagram):
        if light == '#':
            target_config |= (1 << i)
    
    button_masks = []
    for schematic in button_schematics:
        indexes = [int(c) for c in schematic.split(',')]
        mask = [i in indexes for i in range(len(light_diagram))]
        bitmask = sum(bit << index for index, bit in enumerate(mask))
        button_masks.append(bitmask)

    return target_config, button_masks

machine_button_presses = []

for line in machines:
    target_config, button_masks = parse_machine(line)
    def next_configs(current_config):
        for mask in button_masks:
            yield current_config ^ mask

    button_presses = Pathfinding.bfs_distance(
        start_node=0,
        goal_node=target_config,
        get_neighbors_fn=next_configs)

    machine_button_presses.append(button_presses)

total_button_presses = sum(machine_button_presses)
AoCUtils.print_solution(1, total_button_presses)