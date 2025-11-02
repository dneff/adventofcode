#!/usr/bin/env python3
"""
Verify Advent of Code solutions against known correct answers.

This script runs each solution file for a specified year and compares the output
against the answer files stored in aoc-data.

Usage:
    python verify_solutions.py [YEAR]

    YEAR: The year to verify (e.g., 2015, 2016, 2017). Defaults to 2015.
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


def get_expected_answer(day: int, part: int, year: int, base_dir: Path) -> str | None:
    """
    Read the expected answer from aoc-data directory.

    Args:
        day: Day number (1-25)
        part: Part number (1 or 2)
        year: Year (e.g., 2015, 2016, 2017)
        base_dir: Base directory of the adventofcode repo

    Returns:
        Expected answer as string, or None if file doesn't exist or is invalid
    """
    # Path from repo root to aoc-data is ../aoc-data
    answer_file = base_dir.parent / "aoc-data" / str(year) / str(day) / f"solution-{part}"

    if not answer_file.exists():
        return None

    try:
        content = answer_file.read_text().strip()
        # Check if it's a non-zero integer
        if content and content != '0':
            return content
        return None
    except Exception:
        return None


def run_solution(day: int, part: int, year: int) -> tuple[str | None, bool, float]:
    """
    Run a solution file and extract the answer.

    Args:
        day: Day number (1-25)
        part: Part number (1 or 2)
        year: Year (e.g., 2015, 2016, 2017)

    Returns:
        Tuple of (answer, success, elapsed_time) where answer is the solution output or None if failed,
        and elapsed_time is the execution time in seconds
    """
    solution_file = Path(f"python/{year}/{day:02d}/solution{part}.py")

    if not solution_file.exists():
        return None, False, 0.0

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
            return None, False, elapsed_time

        # Extract the answer from output (looking for lines like "Part 1: 138")
        for line in result.stdout.split('\n'):
            if f'Part {part}:' in line:
                answer = line.split(':')[-1].strip()
                return answer, True, elapsed_time

        return None, False, elapsed_time
    except subprocess.TimeoutExpired:
        return None, False, 30.0
    except Exception as e:
        return None, False, 0.0


def main():
    """Run verification for all solutions for a specified year."""
    parser = argparse.ArgumentParser(
        description='Verify Advent of Code solutions against known correct answers.'
    )
    parser.add_argument(
        'year',
        type=int,
        nargs='?',
        default=2015,
        help='Year to verify (default: 2015)'
    )
    args = parser.parse_args()
    year = args.year

    # Validate year
    base_dir = Path(__file__).parent
    python_year_dir = base_dir / "python" / str(year)
    aoc_data_dir = base_dir.parent / "aoc-data" / str(year)

    if not python_year_dir.exists():
        print(f"{RED}Error: Python solutions directory not found for year {year}{RESET}")
        print(f"Expected directory: {python_year_dir}")
        sys.exit(1)

    if not aoc_data_dir.exists():
        print(f"{YELLOW}Warning: aoc-data directory not found for year {year}{RESET}")
        print(f"Expected directory: {aoc_data_dir}")
        print("Continuing anyway, but no answers will be verified.")

    print(f"{BLUE}Verifying {year} Advent of Code Solutions{RESET}")
    print("=" * 60)

    total_verified = 0
    total_correct = 0
    total_incorrect = 0
    total_missing = 0
    total_failed = 0

    for day in range(1, 26):
        for part in [1, 2]:
            expected = get_expected_answer(day, part, year, base_dir)

            if expected is None:
                # No verified answer available
                total_missing += 1
                continue

            actual, success, elapsed_time = run_solution(day, part, year)

            if not success or actual is None:
                print(f"{RED}✗{RESET} Day {day:2d} Part {part}: {RED}FAILED TO RUN{RESET} ({elapsed_time:.3f}s)")
                total_failed += 1
                continue

            total_verified += 1

            if actual == expected:
                print(f"{GREEN}✓{RESET} Day {day:2d} Part {part}: {GREEN}CORRECT{RESET} (answer: {actual}, {elapsed_time:.3f}s)")
                total_correct += 1
            else:
                print(f"{RED}✗{RESET} Day {day:2d} Part {part}: {RED}INCORRECT{RESET} (expected: {expected}, got: {actual}, {elapsed_time:.3f}s)")
                total_incorrect += 1

    # Print summary
    print("\n" + "=" * 60)
    print(f"{BLUE}Summary for {year}:{RESET}")
    print(f"  {GREEN}Correct:{RESET}      {total_correct}")
    print(f"  {RED}Incorrect:{RESET}    {total_incorrect}")
    print(f"  {RED}Failed:{RESET}       {total_failed}")
    print(f"  {YELLOW}Not Verified:{RESET} {total_missing}")
    print(f"  {BLUE}Total Verified:{RESET} {total_verified}")

    if total_incorrect > 0 or total_failed > 0:
        sys.exit(1)
    else:
        print(f"\n{GREEN}All verified solutions are correct!{RESET}")


if __name__ == "__main__":
    main()
