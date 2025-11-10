"""
Advent of Code 2019 - Day 16: Flawed Frequency Transmission - Part 2

The real signal is the input repeated 10,000 times. The message offset is given
by the first 7 digits. Use optimized algorithm since we only need digits after
the offset (which is in the second half where pattern is all 1s).
"""
import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/16/input')


def apply_fft_optimized(signal_data, num_phases=100):
    """
    Apply FFT algorithm optimized for second half of signal.

    When the offset is in the second half, the pattern for each position
    consists only of 1s, so we can use cumulative sum from right to left.

    Args:
        signal_data: Input signal as string
        num_phases: Number of phases to apply

    Returns:
        Output signal as string
    """
    # Repeat signal 10,000 times
    full_signal = signal_data * 10000

    # Get message offset from first 7 digits
    message_offset = int(signal_data[:7])

    # Only process from offset onward (optimization)
    truncated_signal = full_signal[message_offset:]
    signal_digits = [int(digit) for digit in truncated_signal]

    for _ in range(num_phases):
        output_signal = [0] * len(signal_digits)
        # Last digit stays the same
        output_signal[-1] = signal_digits[-1]

        # Work backwards, each position is sum of current + next
        for idx in range(len(signal_digits) - 2, -1, -1):
            output_signal[idx] = (signal_digits[idx] + output_signal[idx + 1]) % 10

        signal_digits = output_signal

    return "".join(str(digit) for digit in output_signal)


def solve_part2():
    """Find 8-digit message in real signal after 100 phases."""
    signal_data = AoCInput.read_file(INPUT_FILE).strip()
    output_signal = apply_fft_optimized(signal_data, 100)
    return output_signal[:8]


answer = solve_part2()
AoCUtils.print_solution(2, answer)
