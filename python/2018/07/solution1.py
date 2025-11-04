"""
Advent of Code 2018 - Day 7: The Sum of Its Parts (Part 1)
https://adventofcode.com/2018/day/7

Determine the order in which to complete sleigh assembly steps based on their
dependencies. Each step is represented by a single letter.

Rules:
- Steps must complete their prerequisites before they can begin
- When multiple steps are ready, choose the one that comes first alphabetically

Input format: "Step C must be finished before step A can begin."
"""

import os
import sys
from collections import defaultdict
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2018/7/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def parse_step_dependencies(lines):
    """
    Parse step dependencies from input lines.

    Args:
        lines: List of dependency descriptions

    Returns:
        tuple: (steps_dict, requirements_dict)
            - steps_dict: step -> list of steps that depend on it
            - requirements_dict: step -> list of prerequisite steps
    """
    steps = defaultdict(list)
    requirements = defaultdict(list)

    for line in lines:
        words = line.strip().split()
        prerequisite = words[1]
        step = words[7]
        steps[prerequisite].append(step)
        requirements[step].append(prerequisite)

    return steps, requirements


def solve_part1():
    """
    Determine the correct order to complete all assembly steps.

    Returns:
        str: Steps in the order they should be completed
    """
    lines = AoCInput.read_lines(INPUT_FILE)
    steps, requirements = parse_step_dependencies(lines)

    # Find steps with no prerequisites (starting steps)
    all_dependent_steps = [step for step_list in steps.values() for step in step_list]
    starting_steps = set(steps.keys()) - set(all_dependent_steps)

    completed_steps = []
    available_steps = list(starting_steps)

    # Process steps in order
    while available_steps:
        # Sort to ensure alphabetical processing
        available_steps.sort()

        # Find the first available step whose requirements are met
        for i, step in enumerate(available_steps):
            if step not in requirements or set(requirements[step]) <= set(completed_steps):
                # This step can be completed
                completed_steps.append(available_steps.pop(i))
                break

        # Add newly available steps
        for completed in completed_steps:
            for dependent_step in steps[completed]:
                if dependent_step not in available_steps and dependent_step not in completed_steps:
                    available_steps.append(dependent_step)

    return ''.join(completed_steps)


# Compute and print the answer for part 1
step_order = solve_part1()
AoCUtils.print_solution(1, step_order)
