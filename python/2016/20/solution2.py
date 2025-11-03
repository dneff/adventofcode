import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/20/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils

def main():
    # Day 20: Firewall Rules - Part 2
    # Problem: Count the total number of IP addresses that are allowed (not blocked)
    # The firewall maintains a blacklist of IP ranges (both endpoints inclusive)
    # We need to find all the gaps between blocked ranges and count the allowed IPs
    # IP addresses are 32-bit integers (0 to 4,294,967,295)

    # Parse the blacklist of blocked IP ranges
    # Key: start of blocked range, Value: end of blocked range (inclusive)
    blocked_ranges = {}
    for line in AoCInput.read_lines(INPUT_FILE):
        range_start, range_end = line.strip().split('-')
        blocked_ranges[int(range_start)] = int(range_end)

    # Track the current IP we're checking and the set of allowed IPs
    current_ip = 0
    allowed_ips = set()

    # Process all blocked ranges to find gaps (allowed IPs)
    while len(blocked_ranges.keys()) > 0:
        # Skip over all blocked ranges that overlap with or touch our current position
        while len(blocked_ranges.keys()) > 0 and min(blocked_ranges.keys()) <= current_ip:
            # Find the next blocked range that starts at or before our current position
            next_blocked_start = min(blocked_ranges.keys())
            next_blocked_end = blocked_ranges[next_blocked_start]

            # Advance past this blocked range (to one position after the range ends)
            current_ip = max(current_ip, next_blocked_end + 1)

            # Remove this processed range from our dictionary
            blocked_ranges.pop(next_blocked_start)

        # If there are still blocked ranges remaining, we found a gap
        # The current_ip is in a gap between blocked ranges, so it's allowed
        if len(blocked_ranges.keys()) > 0:
            allowed_ips.add(current_ip)
            current_ip += 1

    # Count the total number of allowed IP addresses
    AoCUtils.print_solution(2, len(allowed_ips))

if __name__ == "__main__":
    main()