"""
Advent of Code 2019 - Day 17: Set and Forget - Part 2

Program the vacuum robot to traverse all scaffolding. The robot needs:
- A main movement routine (max 20 chars)
- Three movement functions A, B, C (each max 20 chars)
- Continuous video feed preference (y/n)

The movement commands are compression of the full path. Return the amount
of dust collected (final output from the program).
"""
import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402
from IntCode import IntCode, OutputInterrupt  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/17/input')


def solve_part2():
    """
    Program the vacuum robot with movement routines to collect dust.

    Note: The movement routines were determined by analyzing the scaffold
    pattern from Part 1 and manually compressing the full path.
    """
    program = AoCInput.read_file(INPUT_FILE).strip()

    # Movement routines (determined by analyzing the scaffold pattern)
    main_routine = "A,B,A,B,A,C,B,C,A,C\n"
    function_a = "L,6,R,12,L,6\n"
    function_b = "R,12,L,10,L,4,L,6\n"
    function_c = "L,10,L,10,L,4,L,6\n"
    video_feed = "n\n"  # Don't show continuous video feed

    # Wake up the robot (set memory[0] to 2)
    vacuum_robot = IntCode(program)
    vacuum_robot.complete = False
    vacuum_robot.memory[0] = 2

    # Input all movement routines
    for routine in [main_routine, function_a, function_b, function_c, video_feed]:
        for char in routine:
            vacuum_robot.push(ord(char))

    # Run robot and collect output
    display_output = []
    while not vacuum_robot.complete:
        try:
            vacuum_robot.run()
        except OutputInterrupt:
            output_char = chr(int(vacuum_robot.pop()))
            display_output.append(output_char)

    # The final output is the amount of dust collected
    dust_collected = ord(display_output[-1])
    return dust_collected


answer = solve_part2()
AoCUtils.print_solution(2, answer)
