"""
Advent of Code 2018 - Day 7: The Sum of Its Parts (Part 2)
https://adventofcode.com/2018/day/7

Simulate multiple workers completing assembly steps in parallel. Each step takes
time to complete: base_time + step_position (A=1, B=2, ..., Z=26).

With 5 workers and a base time of 60 seconds, determine how long it takes to
complete all steps.

Workers can work on different steps simultaneously, and new steps become available
as their prerequisites are completed.
"""

import os
import sys
from collections import defaultdict
from string import ascii_uppercase
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


def get_step_duration(step, base_time=60):
    """
    Calculate how long a step takes to complete.

    Args:
        step: Step letter
        base_time: Base time for all steps

    Returns:
        int: Time in seconds to complete the step
    """
    return ascii_uppercase.find(step) + base_time + 1


def solve_part2():
    """
    Simulate parallel step completion with multiple workers.

    Returns:
        int: Total time in seconds to complete all steps
    """
    lines = AoCInput.read_lines(INPUT_FILE)
    steps, requirements = parse_step_dependencies(lines)

    # Find starting steps
    all_dependent_steps = [step for step_list in steps.values() for step in step_list]
    starting_steps = set(steps.keys()) - set(all_dependent_steps)

    num_workers = 5
    base_time = 60
    completed_steps = []
    active_steps = {}  # step -> remaining time

    # Start with initial steps
    for step in starting_steps:
        active_steps[step] = get_step_duration(step, base_time)

    total_time = 0

    # Simulate work until all steps are complete
    while active_steps or len(completed_steps) < 26:
        # Assign available steps to idle workers
        if len(active_steps) < num_workers:
            available_steps = []

            # Find steps that can now be started
            for completed in completed_steps:
                for dependent_step in steps[completed]:
                    if (dependent_step not in active_steps and
                        dependent_step not in completed_steps):
                        # Check if all requirements are met
                        if (dependent_step not in requirements or
                            set(requirements[dependent_step]) <= set(completed_steps)):
                            available_steps.append(dependent_step)

            available_steps.sort()

            # Assign steps to workers
            while available_steps and len(active_steps) < num_workers:
                new_step = available_steps.pop(0)
                active_steps[new_step] = get_step_duration(new_step, base_time)

        # Work for one second
        for step in list(active_steps.keys()):
            active_steps[step] -= 1
            if active_steps[step] <= 0:
                # Step completed
                active_steps.pop(step)
                completed_steps.append(step)

        total_time += 1

    return total_time


# Compute and print the answer for part 2
completion_time = solve_part2()
AoCUtils.print_solution(2, completion_time)
