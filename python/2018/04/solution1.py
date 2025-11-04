"""
Advent of Code 2018 - Day 4: Repose Record (Part 1)
https://adventofcode.com/2018/day/4

Analyze guard shift logs to identify sleep patterns.

Strategy 1: Find the guard who sleeps the most total minutes, then identify which
specific minute that guard spent asleep most frequently. Multiply the guard's ID
by that minute.

Records format:
- [YYYY-MM-DD HH:MM] Guard #ID begins shift
- [YYYY-MM-DD HH:MM] falls asleep
- [YYYY-MM-DD HH:MM] wakes up

Only the minute portion (00-59) during the midnight hour matters.
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


def solve_part1():
    """
    Find the sleepiest guard and their most common sleep minute.

    Returns:
        int: Guard ID × most frequent sleep minute
    """
    log_entries = sorted(AoCInput.read_lines(INPUT_FILE))
    guard_sleep_minutes = parse_guard_sleep_patterns(log_entries)

    # Find the guard who slept the most total minutes
    guard_total_sleep = [(guard_id, sum(minutes.values()))
                         for guard_id, minutes in guard_sleep_minutes.items()]
    guard_total_sleep.sort(key=lambda x: x[1], reverse=True)
    sleepiest_guard = guard_total_sleep[0][0]

    # Find which minute that guard was asleep most often
    sleepiest_minute = max(guard_sleep_minutes[sleepiest_guard],
                          key=guard_sleep_minutes[sleepiest_guard].get)

    return sleepiest_guard * sleepiest_minute


# Compute and print the answer for part 1
answer = solve_part1()
AoCUtils.print_solution(1, answer)
