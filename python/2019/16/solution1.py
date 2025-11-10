"""
Advent of Code 2019 - Day 16: Flawed Frequency Transmission - Part 1

Apply the Flawed Frequency Transmission (FFT) algorithm to clean up a signal.
Each phase applies a repeating pattern [0, 1, 0, -1] with increasing repetition
for each output position. Run 100 phases and return the first 8 digits.
"""
import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/16/input')


def apply_fft_phases(signal_data, num_phases=1):
    """
    Apply FFT algorithm for specified number of phases.

    Args:
        signal_data: Input signal as string of digits
        num_phases: Number of FFT phases to apply

    Returns:
        Output signal as string
    """
    base_pattern = [0, 1, 0, -1]
    signal_digits = [int(digit) for digit in signal_data]

    for _ in range(num_phases):
        output_signal = []

        for output_position in range(1, len(signal_data) + 1):
            digit_sum = 0

            for i, input_digit in enumerate(signal_digits):
                # Calculate pattern position for this input digit
                pattern_index = ((i + 1) // output_position) % len(base_pattern)
                digit_sum += input_digit * base_pattern[pattern_index]

            # Keep only the ones digit
            output_signal.append(abs(digit_sum) % 10)

        signal_digits = output_signal

    return "".join(str(digit) for digit in output_signal)


def solve_part1():
    """Apply 100 FFT phases and return first 8 digits."""
    signal_data = AoCInput.read_file(INPUT_FILE).strip()
    output_signal = apply_fft_phases(signal_data, 100)
    return output_signal[:8]


answer = solve_part1()
AoCUtils.print_solution(1, answer)
