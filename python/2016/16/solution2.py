import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/16/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402
AoCInput  # noqa: F401


def generate_dragon_curve_data(initial_state, disk_length):
    """
    Generate data using the modified dragon curve algorithm to fill a disk.

    The algorithm repeatedly applies these steps until enough data is generated:
    1. Take current data as 'a'
    2. Make a copy 'b' by reversing 'a' and flipping all bits (0→1, 1→0)
    3. Concatenate: a + '0' + b

    Args:
        initial_state: Starting binary string (e.g., "10000")
        disk_length: Target length of data needed to fill the disk

    Returns:
        Binary string of exactly disk_length characters
    """
    data = initial_state
    while len(data) < disk_length:
        # Apply dragon curve: a + '0' + reversed_inverted(a)
        a = data
        b = a[::-1]  # Reverse the string
        # Invert all bits: 0→1, 1→0 (using intermediate '2' to avoid conflicts)
        b = b.replace('1', '2').replace('0', '1').replace('2', '0')
        data = a + "0" + b

    # Truncate to exact disk length
    return data[:disk_length]


def calculate_checksum(data):
    """
    Calculate the checksum for dragon curve data.

    The checksum algorithm processes pairs of characters:
    - If both characters match (00 or 11) → 1
    - If characters differ (01 or 10) → 0

    This produces a result half the length. The process repeats until
    the checksum has an odd length.

    Args:
        data: Binary string to calculate checksum for

    Returns:
        Checksum string with odd length
    """
    result = data[:]

    # Repeat until checksum has odd length
    while len(result) % 2 == 0:
        # Process pairs of characters
        first_chars = result[::2]   # Characters at even indices (0, 2, 4, ...)
        second_chars = result[1::2]  # Characters at odd indices (1, 3, 5, ...)
        # Check if each pair matches
        pairs_match = [x == y for x, y in zip(first_chars, second_chars)]
        # Convert to binary: matching pairs → '1', differing pairs → '0'
        result = ['1' if matches else '0' for matches in pairs_match]

    return ''.join(result)


def main():
    """
    Solve Day 16: Dragon Checksum

    Generate random-looking data using the modified dragon curve algorithm,
    then compute a checksum to update a security system.
    """
    # Test case from problem description
    test_case = {  # noqa: F841
        'init': "10000",
        'length': 20
    }

    # Part 1: Fill a disk of length 272
    part_1 = {  # noqa: F841
        'init': "11011110011011101",
        'length': 272
    }

    # Part 2: Fill a much larger disk
    part_2 = {
        'init': "11011110011011101",
        'length': 35651584
    }

    # Select which puzzle to solve
    active_puzzle = part_2

    # Generate dragon curve data to fill the disk
    disk_data = generate_dragon_curve_data(active_puzzle['init'], active_puzzle['length'])
    # Calculate the checksum for the generated data
    checksum = calculate_checksum(disk_data)

    AoCUtils.print_solution(2, checksum)


if __name__ == "__main__":
    main()
