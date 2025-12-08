"""
Advent of Code 2025 - Day 8: Playground
https://adventofcode.com/2025/day/8

Across the playground, a group of Elves have suspended a large number of 
small electrical junction boxes. Their plan is to connect the junction boxes 
with long strings of lights. 

The Elves are trying to figure out which junction boxes to connect so that 
electricity can reach every junction box. They even have a list of all of the 
junction boxes' positions in 3D space (your puzzle input).

Part 2
Continue connecting the closest unconnected pairs of junction boxes together 
until they're all in the same circuit. What do you get if you multiply 
together the X coordinates of the last two junction boxes you need to connect?

"""

import os
import sys


# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "../../"))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, "../../../../aoc-data/2025/8/input")
position_list = AoCInput.read_lines(INPUT_FILE)

def get_positions(position_list):
    """Parse a list of position strings in the format 'x,y,z' and return a list of (x, y, z) tuples."""
    positions = [(int(x), int(y), int(z)) for pos in position_list for x, y, z in [pos.split(',')]]
    return positions


def find_distance(pos1, pos2):
    """Calculate the Euclidean distance between two 3D points."""
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2 + (pos1[2] - pos2[2]) ** 2) ** 0.5


# Parse all junction box positions from input
junction_positions = get_positions(position_list)

# Calculate Euclidean distances between all pairs of junction boxes
# Store as {(position1, position2): distance} for later sorting
junction_distances = {}
for i in range(len(junction_positions)):
    for j in range(i + 1, len(junction_positions)):
        distance = find_distance(junction_positions[i], junction_positions[j])
        junction_distances[(junction_positions[i], junction_positions[j])] = distance

# Connect junction box pairs in order of increasing distance until all boxes are in one circuit
# This implements a minimum spanning tree algorithm (similar to Kruskal's algorithm)
# We track which circuit each junction belongs to and merge circuits when needed
circuits = []
last_connection = None

for junction_pair, distance in sorted(junction_distances.items(), key=lambda item: item[1]):
    junction1, junction2 = junction_pair

    # Find which circuits (if any) contain these junctions
    circuit1_idx = None
    circuit2_idx = None
    for idx, circuit in enumerate(circuits):
        if junction1 in circuit:
            circuit1_idx = idx
        if junction2 in circuit:
            circuit2_idx = idx

    # Handle the different connection cases
    if circuit1_idx is None and circuit2_idx is None:
        # Neither junction is in a circuit yet - create a new circuit
        circuits.append({junction1, junction2})
        last_connection = (junction1, junction2)
    elif circuit1_idx == circuit2_idx and circuit1_idx is not None:
        # Both junctions are already in the same circuit - skip this connection
        continue
    elif circuit1_idx is None:
        # Only junction2 has a circuit - add junction1 to it
        circuits[circuit2_idx].add(junction1)
        last_connection = (junction1, junction2)
    elif circuit2_idx is None:
        # Only junction1 has a circuit - add junction2 to it
        circuits[circuit1_idx].add(junction2)
        last_connection = (junction1, junction2)
    else:
        # Both junctions are in different circuits - merge them
        circuits[circuit1_idx].update(circuits[circuit2_idx])
        del circuits[circuit2_idx]
        last_connection = (junction1, junction2)

    # Check if all junction boxes are now in a single circuit
    total_junctions_in_circuits = sum(len(circuit) for circuit in circuits)
    if len(circuits) == 1 and total_junctions_in_circuits == len(junction_positions):
        # All junctions are connected - we're done
        break

# Calculate the product of the X coordinates of the last two junctions connected
result = last_connection[0][0] * last_connection[1][0]
AoCUtils.print_solution(2, result)