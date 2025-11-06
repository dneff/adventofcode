"""
Advent of Code 2016 - Day 15: Timing is Everything (Part 2)

Find the first time to press a button so that a capsule can fall through
all rotating discs in a kinetic sculpture. Each disc has a slot at position 0
and rotates one position per second. The capsule must pass through each disc
when its slot is aligned (at position 0).

Part 2: An additional disc appears at the bottom with 11 positions, starting at position 0.
"""
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/15/input')

sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils, MathUtils  # noqa: E402


def get_disc_position(num_positions, start_position, time):
    """
    Calculate the position of a disc at a given time.

    Args:
        num_positions: Total number of positions on the disc
        start_position: The disc's position at time=0
        time: The time at which to calculate the position

    Returns:
        The disc's position at the given time (0 means slot is aligned)
    """
    return (start_position + time) % num_positions


def main():
    # Parse input to build the kinetic sculpture's disc configuration
    # Each disc has a number of positions and a starting position
    discs = {}
    input_lines = AoCInput.read_lines(INPUT_FILE)

    for disc_index, line in enumerate(input_lines):
        # Parse line: "Disc #N has X positions; at time=0, it is at position Y."
        tokens = line.strip().split()
        discs[disc_index] = {
            'num_positions': int(tokens[3]),
            'start_position': int(tokens[-1][:-1])  # Remove trailing period
        }

    # Part 2: Add an additional disc with 11 positions, starting at position 0
    discs[len(discs)] = {'num_positions': 11, 'start_position': 0}

    # Optimized approach: Incremental constraint satisfaction
    # Once we satisfy disc N, we can step by the LCM of all previous periods
    # to keep all previous discs satisfied while checking the next disc
    button_time = 0
    step_size = 1  # Start by checking every time

    for disc_index in range(len(discs)):
        # Find the next time that satisfies this disc
        while True:
            disc_position = get_disc_position(
                discs[disc_index]['num_positions'],
                discs[disc_index]['start_position'],
                button_time + disc_index + 1
            )

            if disc_position == 0:
                # This disc is satisfied! Update step size to keep all satisfied discs aligned
                step_size = MathUtils.lcm(step_size, discs[disc_index]['num_positions'])
                break

            button_time += step_size

    AoCUtils.print_solution(2, button_time)


if __name__ == "__main__":
    main()
