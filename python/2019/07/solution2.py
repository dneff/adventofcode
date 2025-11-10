"""
Advent of Code 2019 - Day 7: Amplification Circuit - Part 2

Find the maximum thruster signal using a feedback loop configuration.
The five amplifiers are connected in a loop (E feeds back to A), using
phase settings 5-9. Each amplifier pauses when waiting for input or after
producing output, allowing the signal to loop through all amplifiers
repeatedly until all halt.
"""
import os
import sys
from itertools import permutations

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402
from IntCode import IntCode, InputInterrupt, OutputInterrupt  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/7/input')


def run_amplifier_feedback_loop(program, phase_sequence):
    """
    Run amplifiers in feedback loop mode with the given phase sequence.

    Args:
        program: The Intcode program string
        phase_sequence: Tuple of 5 phase settings (5-9)

    Returns:
        The final thruster signal when all amplifiers halt
    """
    # Create five amplifier computers
    amplifiers = []
    for phase in phase_sequence:
        amp = IntCode(program)
        amp.push(phase)
        amplifiers.append(amp)

    # Initialize first amplifier with signal 0
    amplifiers[0].push(0)

    # Run amplifiers in round-robin until all complete
    current_amp_index = 0
    while True:
        current_amp = amplifiers[current_amp_index]

        if current_amp.complete:
            # Move to next amplifier
            current_amp_index = (current_amp_index + 1) % 5
            # Check if all amplifiers are complete
            if all(amp.complete for amp in amplifiers):
                break
            continue

        try:
            # Run current amplifier until it halts or needs input/output
            current_amp.run()
        except OutputInterrupt:
            # Amplifier produced output, send to next amplifier
            output_signal = current_amp.pop()
            next_amp_index = (current_amp_index + 1) % 5
            amplifiers[next_amp_index].push(output_signal)
        except InputInterrupt:
            # Amplifier waiting for input, switch to next one
            current_amp_index = (current_amp_index + 1) % 5

    # The final signal is the last value sent to amplifier A (index 0)
    return amplifiers[0].input[-1]


def solve_part2():
    """Find maximum thruster signal using feedback loop configuration."""
    content = AoCInput.read_file(INPUT_FILE)

    max_thruster_signal = 0
    phase_settings = [5, 6, 7, 8, 9]

    # Try all permutations of feedback loop phase settings
    for phase_sequence in permutations(phase_settings):
        signal = run_amplifier_feedback_loop(content.strip(), phase_sequence)
        max_thruster_signal = max(max_thruster_signal, signal)

    return max_thruster_signal


answer = solve_part2()
AoCUtils.print_solution(2, answer)
