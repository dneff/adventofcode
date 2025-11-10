"""
Advent of Code 2019 - Day 6: Universal Orbit Map - Part 2

Find the minimum number of orbital transfers required to move from the object YOU
are orbiting to the object Santa (SAN) is orbiting. Count the number of orbital
transfers (not the number of objects visited).
"""
import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/6/input')


def get_orbit_chain(orbit_map, start_object, end_object):
    """
    Build a chain of objects from start_object to end_object following orbits.

    Args:
        orbit_map: Dictionary mapping object -> what it orbits
        start_object: Starting object (orbiter)
        end_object: Destination object (typically COM)

    Returns:
        List of objects from start_object to end_object
    """
    chain = [start_object]
    if orbit_map[start_object] == end_object:
        chain.append(end_object)
    else:
        chain.extend(get_orbit_chain(orbit_map, orbit_map[start_object], end_object))
    return chain


def build_orbit_map(lines):
    """
    Parse orbit data into a map of object -> what it orbits.

    Args:
        lines: Input lines in format "A)B" meaning B orbits A

    Returns:
        Dictionary mapping each orbiting object to its parent
    """
    orbit_map = {}
    for line in lines:
        parent, orbiter = line.strip().split(')')
        orbit_map[orbiter] = parent
    return orbit_map


def solve_part2():
    """
    Find minimum orbital transfers from YOU's orbit to SAN's orbit.

    This works by finding the paths from YOU and SAN to COM, then removing
    the common suffix (the shared ancestor chain). The remaining path segments
    represent the transfers needed.
    """
    lines = AoCInput.read_lines(INPUT_FILE)
    orbit_map = build_orbit_map(lines)

    # Get paths from YOU and SAN to COM
    you_path = get_orbit_chain(orbit_map, 'YOU', 'COM')
    santa_path = get_orbit_chain(orbit_map, 'SAN', 'COM')

    # Remove common ancestors from both paths
    # We check [-2] because we want to find the last common ancestor before divergence
    while len(you_path) >= 2 and len(santa_path) >= 2 and you_path[-2] == santa_path[-2]:
        you_path.pop()
        santa_path.pop()

    # Total transfers = path lengths - YOU - SAN - 2 (we count edges, not nodes)
    # -2 accounts for YOU and SAN themselves, -2 more for the two endpoints
    total_transfers = len(you_path) + len(santa_path) - 4

    return total_transfers


answer = solve_part2()
AoCUtils.print_solution(2, answer)
