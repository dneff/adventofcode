"""
Advent of Code 2025 - Day 8: Playground
https://adventofcode.com/2025/day/8

Across the playground, a group of Elves have suspended a large number of 
small electrical junction boxes. Their plan is to connect the junction boxes 
with long strings of lights. 

The Elves are trying to figure out which junction boxes to connect so that 
electricity can reach every junction box. They even have a list of all of the 
junction boxes' positions in 3D space (your puzzle input).

Part 1
Your list contains many junction boxes; connect together the 1000 pairs of 
junction boxes which are closest together. Afterward, what do you get if you 
multiply together the sizes of the three largest circuits?

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

# Connect the closest 1000 pairs of junction boxes and group them into circuits
# Each circuit is a set of junction boxes that are connected together
# This implements a union-find-like approach where connected boxes merge into the same circuit
circuits = []

for junction_pair, distance in sorted(junction_distances.items(), key=lambda item: item[1])[:1000]:
    junction1, junction2 = junction_pair

    # Check if either junction is already in an existing circuit
    existing_circuit = None
    for circuit in circuits:
        if junction1 in circuit or junction2 in circuit:
            existing_circuit = circuit
            break

    if existing_circuit:
        # Add both junctions to the existing circuit (one may already be there)
        existing_circuit.update([junction1, junction2])
    else:
        # Neither junction is in a circuit yet, so create a new one
        circuits.append(set([junction1, junction2]))

# Merge circuits that share any junction boxes
# This is necessary because our initial pass may have created separate circuits
# that should actually be connected (e.g., if A-B and B-C were added separately)
merged = True
while merged:
    merged = False
    for i in range(len(circuits)):
        for j in range(i + 1, len(circuits)):
            if circuits[i].intersection(circuits[j]):
                # Merge circuit j into circuit i
                circuits[i].update(circuits[j])
                del circuits[j]
                merged = True
                break
        if merged:
            break

print(f"Total circuits formed: {[len(circuit) for circuit in circuits]}")

# Calculate the product of the three largest circuit sizes
circuit_sizes = sorted([len(circuit) for circuit in circuits], reverse=True)
result = circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]

AoCUtils.print_solution(1, result)

