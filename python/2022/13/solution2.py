"""
Advent of Code 2022 - Day 13: Distress Signal (Part 2)
https://adventofcode.com/2022/day/13

Sort all packets including divider packets [[2]] and [[6]],
then find the decoder key by multiplying the positions of the dividers.
"""

import os
import sys
from copy import deepcopy as dc

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2022/13/input')


def compare(left, right):
    """
    Compare two packet values according to the distress signal protocol.

    If both are integers:
        - If left < right, return 1 (correct order)
        - If left > right, return -1 (wrong order)
        - Otherwise, return 0 (continue checking)

    If both are lists:
        - Compare element by element
        - If left runs out first, return 1 (correct order)
        - If right runs out first, return -1 (wrong order)
        - Otherwise, return 0 (continue checking)

    If exactly one is an integer:
        - Convert integer to list and retry comparison

    Args:
        left: Left packet value (int or list)
        right: Right packet value (int or list)

    Returns:
        int: -1 (wrong order), 0 (equal/unknown), 1 (correct order)
    """
    FALSE = -1
    UNKNOWN = 0
    TRUE = 1

    # Both are integers
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return TRUE
        elif left > right:
            return FALSE
        return UNKNOWN

    # Both are lists
    if isinstance(left, list) and isinstance(right, list):
        while len(left) != 0:
            if len(right) == 0:
                return FALSE
            test = compare(left.pop(0), right.pop(0))
            if test != UNKNOWN:
                return test

        if len(right) != 0:
            return TRUE
        return UNKNOWN

    # One is integer, one is list - convert integer to list
    if isinstance(left, int):
        left = [left]
    if isinstance(right, int):
        right = [right]

    return compare(left, right)


def insert_packet(packet, sorted_list):
    """
    Insert a packet into the sorted list in the correct position.

    Args:
        packet: Packet to insert
        sorted_list: List of packets in sorted order
    """
    if len(sorted_list) != 0:
        for idx, pkt in enumerate(sorted_list):
            if compare(dc(pkt), dc(packet)) == 0:
                return
            if compare(dc(pkt), dc(packet)) < 0:
                sorted_list.insert(idx, dc(packet))
                return
    sorted_list.append(dc(packet))


def solve_part2():
    """
    Sort all packets with dividers and find the decoder key.

    Returns:
        int: Product of 1-based positions of divider packets [[2]] and [[6]]
    """
    lines = AoCInput.read_lines(INPUT_FILE)

    sorted_packets = []
    divider_1 = [[2]]
    divider_2 = [[6]]

    # Insert divider packets
    insert_packet(dc(divider_1), sorted_packets)
    insert_packet(dc(divider_2), sorted_packets)

    # Insert all other packets
    for line in lines:
        if len(line.strip()) == 0:
            continue
        packet = eval(line)
        insert_packet(dc(packet), sorted_packets)

    # Find positions of dividers (1-based index)
    idx_d1 = sorted_packets.index(divider_1) + 1
    idx_d2 = sorted_packets.index(divider_2) + 1

    return idx_d1 * idx_d2


# Compute and print the answer for part 2
answer = solve_part2()
AoCUtils.print_solution(2, answer)
