"""
Advent of Code 2018 - Day 20: A Regular Map (Part 2)
https://adventofcode.com/2018/day/20

Part 2 asks how many rooms have a shortest path of at least 1000 doors from your starting position.
"""
import os
import sys
import networkx

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2018/20/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))
from aoc_helpers import AoCUtils


def get_new_position(position, move):
    """
    Calculate new position based on current position and direction.
    Returns tuple of (x, y) coordinates.
    """
    direction = {'N': (0, 1), 'E': (-1, 0), 'S': (0, -1), 'W': (1, 0)}
    if move not in direction:
        raise ValueError(f"Invalid direction {move}")
    x = position[0] + direction[move][0]
    y = position[1] + direction[move][1]
    return (x, y)


def main():
    """
    Parse the regex pattern to build a map of rooms and doors,
    then count how many rooms require at least 1000 doors to reach.
    """
    file = open(INPUT_FILE, 'r', encoding='utf-8')
    moves = file.readline().strip()
    # Remove the outer ^ and $ from the regex
    moves = moves[1:-1]

    # Build a graph of rooms and doors
    stack = []
    elf_map = networkx.Graph()
    start = (0, 0)
    position = {start}  # Current positions in the regex traversal
    start_positions = {start}  # Positions at the start of current group
    end_positions = set()  # Positions at the end of branches

    # Parse the regex pattern
    for move in moves:
        if move == '|':
            # Branch: save current positions and reset to start of group
            end_positions.update(position)
            position = start_positions
        elif move in 'NSEW':
            # Move: add edges for all current positions
            elf_map.add_edges_from((p, get_new_position(p, move)) for p in position)
            position = {get_new_position(p, move) for p in position}
        elif move == '(':
            # Start of group: push current state to stack
            stack.append((start_positions, end_positions))
            start_positions, end_positions = position, set()
        elif move == ')':
            # End of group: merge positions and pop stack
            position.update(end_positions)
            start_positions, end_positions = stack.pop()

    # Find shortest path lengths from start to all rooms
    lengths = networkx.algorithms.shortest_path_length(elf_map, (0, 0))

    # Count rooms requiring at least 1000 doors
    qualifying_lengths = [x for x in lengths.values() if x >= 1000]
    AoCUtils.print_solution(2, len(qualifying_lengths))


if __name__ == "__main__":
    main()
