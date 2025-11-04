"""
Advent of Code 2018 - Day 4: Repose Record (Part 2)
https://adventofcode.com/2018/day/4

Analyze guard shift logs using a different strategy.

Strategy 2: Find the guard who is most frequently asleep on the same minute
across all nights. Multiply the guard's ID by that minute.

This finds the guard/minute combination with the highest frequency of sleep.
"""

import os
import sys
from collections import defaultdict
from datetime import datetime
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2018/4/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils


def parse_guard_sleep_patterns(log_entries):
    """
    Parse guard logs and build sleep pattern data.

    Args:
        log_entries: List of chronologically sorted log entries

    Returns:
        dict: Guard ID -> {minute -> count of times asleep at that minute}
    """
    date_format = '%Y-%m-%d %H:%M'
    guard_sleep_minutes = defaultdict(lambda: defaultdict(int))
    current_guard = None

    idx = 0
    while idx < len(log_entries):
        entry = log_entries[idx].split()

        if entry[2] == 'Guard':
            # New guard begins shift
            current_guard = int(entry[3][1:])  # Remove '#' prefix
        elif entry[2] == 'falls':
            # Guard falls asleep - parse start time
            sleep_start = log_entries[idx].split(']')[0][1:]
            sleep_start = datetime.strptime(sleep_start, date_format)

            # Next entry should be wake up time
            idx += 1
            sleep_end = log_entries[idx].split(']')[0][1:]
            sleep_end = datetime.strptime(sleep_end, date_format)

            # Mark each minute asleep
            for minute in range(sleep_start.minute, sleep_end.minute):
                guard_sleep_minutes[current_guard][minute] += 1

        idx += 1

    return guard_sleep_minutes


def solve_part2():
    """
    Find the guard/minute combination with the highest sleep frequency.

    Returns:
        int: Guard ID × minute with most frequent sleep
    """
    log_entries = sorted(AoCInput.read_lines(INPUT_FILE))
    guard_sleep_minutes = parse_guard_sleep_patterns(log_entries)

    # For each guard, find their most frequent sleep minute and its count
    guard_peak_minutes = []
    for guard_id in guard_sleep_minutes.keys():
        most_frequent_minute = max(guard_sleep_minutes[guard_id],
                                  key=guard_sleep_minutes[guard_id].get)
        frequency = guard_sleep_minutes[guard_id][most_frequent_minute]
        guard_peak_minutes.append((guard_id, most_frequent_minute, frequency))

    # Find the guard/minute with the highest frequency
    guard_peak_minutes.sort(key=lambda x: x[2], reverse=True)
    best_guard = guard_peak_minutes[0][0]
    best_minute = guard_peak_minutes[0][1]

    return best_guard * best_minute


# Compute and print the answer for part 2
answer = solve_part2()
AoCUtils.print_solution(2, answer)
