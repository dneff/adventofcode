import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/20/input')

sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402


def main():
    # Day 20: Firewall Rules - Part 1
    # Problem: Find the lowest-valued IP address that is not blocked by the firewall
    # The firewall maintains a blacklist of IP ranges (both endpoints inclusive)
    # IP addresses are 32-bit integers (0 to 4, 294, 967, 295)
    # Example: Ranges "5-8", "0-2", "4-7" would allow IPs 3 and 9, so lowest is 3

    # Parse the blacklist of blocked IP ranges
    # Key: start of blocked range, Value: end of blocked range (inclusive)
    blocked_ranges = {}

    for line in AoCInput.read_lines(INPUT_FILE):
        range_start, range_end = line.strip().split('-')
        blocked_ranges[int(range_start)] = int(range_end)

    # Track the lowest IP we're checking for availability
    # Start at 0 and work our way up, skipping blocked ranges
    lowest_allowed_ip = 0

    # Process blocked ranges that could affect our current candidate IP
    # Keep advancing past blocked ranges until we find a gap
    while min(blocked_ranges.keys()) <= lowest_allowed_ip:
        # Find the next blocked range that starts at or before our current position
        next_blocked_start = min(blocked_ranges.keys())
        next_blocked_end = blocked_ranges[next_blocked_start]

        # Advance past this blocked range (to one position after the range ends)
        lowest_allowed_ip = max(lowest_allowed_ip, next_blocked_end + 1)

        # Remove this processed range from our dictionary
        blocked_ranges.pop(next_blocked_start)

    # The lowest_allowed_ip is now the first IP not blocked by any range
    AoCUtils.print_solution(1, lowest_allowed_ip)


if __name__ == "__main__":
    main()
