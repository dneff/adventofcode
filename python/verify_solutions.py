#!/usr/bin/env python3
"""
Verify Advent of Code solutions against known correct answers.

This script runs each solution file for a specified year and compares the output
against the answer files stored in aoc-data.

Usage:
    python python/verify_solutions.py [YEAR] [DAY] [OPTIONS]

Positional Arguments:
    YEAR                      The year to verify (e.g., 2015, 2016, 2017)
    DAY                       The day to verify (1-25)

Options:
    --year YEAR, -y YEAR      The year to verify (alternative to positional)
    --day DAY, -d DAY         The day to verify (alternative to positional)
    --write-missing, -w       Write solution output to missing answer files

Examples:
    python python/verify_solutions.py              # Verify all years
    python python/verify_solutions.py 2015         # Verify year 2015
    python python/verify_solutions.py 2015 20      # Verify year 2015, day 20
    python python/verify_solutions.py --year 2015 --day 20 --write-missing

If no year is specified, all years will be verified.
If no day is specified, all days will be verified.
"""

import os
import sys
import subprocess
import time
import argparse
from pathlib import Path

# Colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def get_time_emoji(elapsed_time: float) -> str:
    """
    Get an emoji based on the execution time.

    Args:
        elapsed_time: Execution time in seconds

    Returns:
        Emoji string representing the speed
    """
    if elapsed_time < 1.0:
        return "⚡"
    elif elapsed_time < 3.0:
        return "🚀"
    elif elapsed_time < 10.0:
        return "▶️"
    elif elapsed_time < 30.0:
        return "🐢"
    else:
        return "🐌"


def get_expected_answer(day: int, part: int, year: int, base_dir: Path) -> str | None:
    """
    Read the expected answer from aoc-data directory.

    Args:
        day: Day number (1-25)
        part: Part number (1 or 2)
        year: Year (e.g., 2015, 2016, 2017)
        base_dir: Base directory of the adventofcode repo

    Returns:
        Expected answer as string, or None if file doesn't exist or is empty
    """
    # Path from python/ dir to aoc-data is ../../aoc-data
    answer_file = base_dir.parent.parent / "aoc-data" / str(year) / str(day) / f"solution-{part}"

    if not answer_file.exists():
        return None

    try:
        content = answer_file.read_text().strip()
        # Return None if empty or just '0'
        if content and content != '0':
            return content
        return None
    except Exception:
        return None


def write_answer(day: int, part: int, year: int, answer: str, base_dir: Path) -> bool:
    """
    Write an answer to the aoc-data directory.

    Args:
        day: Day number (1-25)
        part: Part number (1 or 2)
        year: Year (e.g., 2015, 2016, 2017)
        answer: The answer to write
        base_dir: Base directory of the adventofcode repo

    Returns:
        True if successfully written, False otherwise
    """
    # Path from python/ dir to aoc-data is ../../aoc-data
    answer_dir = base_dir.parent.parent / "aoc-data" / str(year) / str(day)
    answer_file = answer_dir / f"solution-{part}"

    try:
        # Create directory if it doesn't exist
        answer_dir.mkdir(parents=True, exist_ok=True)

        # Write the answer
        answer_file.write_text(answer.strip() + '\n')
        return True
    except Exception as e:
        print(f"{RED}Error writing answer: {e}{RESET}")
        return False


def run_solution(day: int, part: int, year: int, base_dir: Path) -> tuple[str | None, bool, float, bool]:
    """
    Run a solution file and extract the answer.

    Args:
        day: Day number (1-25)
        part: Part number (1 or 2)
        year: Year (e.g., 2015, 2016, 2017)
        base_dir: Base directory of the python solutions

    Returns:
        Tuple of (answer, success, elapsed_time, file_exists) where:
        - answer is the solution output or None if failed
        - success is True if the solution ran successfully
        - elapsed_time is the execution time in seconds
        - file_exists is True if the solution file exists
    """
    solution_file = base_dir / str(year) / f"{day:02d}" / f"solution{part}.py"

    if not solution_file.exists():
        return None, False, 0.0, False

    try:
        start_time = time.time()
        result = subprocess.run(
            [sys.executable, str(solution_file)],
            capture_output=True,
            text=True,
            timeout=30
        )
        elapsed_time = time.time() - start_time

        if result.returncode != 0:
            return None, False, elapsed_time, True

        # Extract the answer from output (looking for lines like "Part 1: 138")
        for line in result.stdout.split('\n'):
            if f'Part {part}:' in line:
                answer = line.split(':')[-1].strip()
                return answer, True, elapsed_time, True

        return None, False, elapsed_time, True
    except subprocess.TimeoutExpired:
        return None, False, 30.0, True
    except Exception:
        return None, False, 0.0, True


def get_years_to_verify(base_dir: Path, year: int | None) -> list[int]:
    """
    Get the list of years to verify.

    Args:
        base_dir: Base directory of the adventofcode repo
        year: Specific year to verify, or None for all years

    Returns:
        List of years to verify
    """
    if year is not None:
        return [year]

    # Find all years with python solutions (base_dir is already python/)
    if not base_dir.exists():
        return []

    years = []
    for item in base_dir.iterdir():
        if item.is_dir() and item.name.isdigit():
            years.append(int(item.name))

    return sorted(years)


def main():
    """Run verification for all solutions for a specified year."""
    parser = argparse.ArgumentParser(
        description='Verify Advent of Code solutions against known correct answers.'
    )
    parser.add_argument(
        'year_pos',
        nargs='?',
        type=int,
        help='Year to verify (e.g., 2015)',
        metavar='YEAR'
    )
    parser.add_argument(
        'day_pos',
        nargs='?',
        type=int,
        help='Day to verify (1-25)',
        metavar='DAY'
    )
    parser.add_argument(
        '--year', '-y',
        type=int,
        dest='year_flag',
        help='Year to verify (e.g., 2015). If not specified, all years will be verified.'
    )
    parser.add_argument(
        '--day', '-d',
        type=int,
        dest='day_flag',
        help='Day to verify (1-25). If not specified, all days will be verified.'
    )
    parser.add_argument(
        '--write-missing', '-w',
        action='store_true',
        help='Write solution output to missing answer files'
    )
    args = parser.parse_args()

    # Prioritize positional arguments over flags
    year = args.year_pos if args.year_pos is not None else args.year_flag
    day = args.day_pos if args.day_pos is not None else args.day_flag

    base_dir = Path(__file__).parent
    years_to_verify = get_years_to_verify(base_dir, year)

    if not years_to_verify:
        print(f"{RED}Error: No Python solutions directories found{RESET}")
        sys.exit(1)

    # Determine days to verify
    if day is not None:
        if not 1 <= day <= 25:
            print(f"{RED}Error: Day must be between 1 and 25{RESET}")
            sys.exit(1)
        days_to_verify = [day]
    else:
        days_to_verify = list(range(1, 26))

    # Verify all years
    all_total_verified = 0
    all_total_correct = 0
    all_total_incorrect = 0
    all_total_missing = 0
    all_total_failed = 0

    for year in years_to_verify:
        python_year_dir = base_dir / str(year)
        aoc_data_dir = base_dir.parent.parent / "aoc-data" / str(year)

        if not python_year_dir.exists():
            print(f"{RED}Error: Python solutions directory not found for year {year}{RESET}")
            print(f"Expected directory: {python_year_dir}")
            continue

        if not aoc_data_dir.exists() and not args.write_missing:
            print(f"{YELLOW}Warning: aoc-data directory not found for year {year}{RESET}")
            print(f"Expected directory: {aoc_data_dir}")
            print("Continuing anyway, but no answers will be verified.")

        if len(years_to_verify) > 1:
            print(f"\n{BLUE}Verifying {year} Advent of Code Solutions{RESET}")
            print("=" * 60)
        else:
            print(f"{BLUE}Verifying {year} Advent of Code Solutions{RESET}")
            print("=" * 60)

        total_verified = 0
        total_correct = 0
        total_incorrect = 0
        total_missing = 0
        total_failed = 0
        total_written = 0

        for day in days_to_verify:
            for part in [1, 2]:
                expected = get_expected_answer(day, part, year, base_dir)

                # Run the solution
                actual, success, elapsed_time, file_exists = run_solution(day, part, year, base_dir)

                # Case 1: Solution file doesn't exist and answer file doesn't exist
                # -> Skip entirely, no output, no counting
                if not file_exists and expected is None:
                    continue

                # Case 2: Solution file doesn't exist but answer file exists
                # -> Show MISSING status (solution file is missing)
                if not file_exists and expected is not None:
                    print(f"{YELLOW}○{RESET} Day {day:2d} Part {part}: {YELLOW}MISSING{RESET} (solution file not found)")
                    total_missing += 1
                    continue

                # Case 3: Solution file exists but failed to run
                if file_exists and (not success or actual is None):
                    emoji = get_time_emoji(elapsed_time)
                    print(f"{RED}✗{RESET} Day {day:2d} Part {part}: {RED}FAILED TO RUN{RESET} ({elapsed_time:.3f}s) {emoji}")
                    total_failed += 1
                    continue

                # Case 4: Solution ran successfully but no expected answer
                # -> Show MISSING status (answer is missing)
                if expected is None:
                    emoji = get_time_emoji(elapsed_time)
                    status_msg = f"{YELLOW}MISSING{RESET}"

                    # Write to answer file if requested
                    if args.write_missing:
                        if write_answer(day, part, year, actual, base_dir):
                            status_msg = f"{YELLOW}MISSING (wrote: {actual}){RESET}"
                            total_written += 1
                        else:
                            status_msg = f"{YELLOW}MISSING (failed to write){RESET}"

                    print(f"{YELLOW}○{RESET} Day {day:2d} Part {part}: {status_msg} (answer: {actual}, {elapsed_time:.3f}s) {emoji}")
                    total_missing += 1
                    continue

                # Case 5: Solution ran successfully and has expected answer
                # -> Compare and show CORRECT/INCORRECT
                total_verified += 1

                if actual == expected:
                    emoji = get_time_emoji(elapsed_time)
                    print(f"{GREEN}✓{RESET} Day {day:2d} Part {part}: {GREEN}CORRECT{RESET} (answer: {actual}, {elapsed_time:.3f}s) {emoji}")
                    total_correct += 1
                else:
                    emoji = get_time_emoji(elapsed_time)
                    print(f"{RED}✗{RESET} Day {day:2d} Part {part}: {RED}INCORRECT{RESET} (expected: {expected}, got: {actual}, {elapsed_time:.3f}s) {emoji}")
                    total_incorrect += 1

        # Print summary for this year
        print("\n" + "=" * 60)
        print(f"{BLUE}Summary for {year}:{RESET}")
        print(f"  {GREEN}Correct:{RESET}      {total_correct}")
        print(f"  {RED}Incorrect:{RESET}    {total_incorrect}")
        print(f"  {RED}Failed:{RESET}       {total_failed}")
        print(f"  {YELLOW}Missing:{RESET}      {total_missing}")
        if args.write_missing and total_written > 0:
            print(f"  {YELLOW}Written:{RESET}      {total_written}")
        print(f"  {BLUE}Total Verified:{RESET} {total_verified}")

        all_total_verified += total_verified
        all_total_correct += total_correct
        all_total_incorrect += total_incorrect
        all_total_missing += total_missing
        all_total_failed += total_failed

    # Print overall summary if multiple years
    if len(years_to_verify) > 1:
        print("\n" + "=" * 60)
        print(f"{BLUE}Overall Summary:{RESET}")
        print(f"  {GREEN}Correct:{RESET}      {all_total_correct}")
        print(f"  {RED}Incorrect:{RESET}    {all_total_incorrect}")
        print(f"  {RED}Failed:{RESET}       {all_total_failed}")
        print(f"  {YELLOW}Missing:{RESET}      {all_total_missing}")
        print(f"  {BLUE}Total Verified:{RESET} {all_total_verified}")

    if all_total_incorrect > 0 or all_total_failed > 0:
        sys.exit(1)
    else:
        if all_total_verified > 0:
            print(f"\n{GREEN}All verified solutions are correct!{RESET}")
        else:
            print(f"\n{YELLOW}No solutions were verified.{RESET}")


if __name__ == "__main__":
    main()
