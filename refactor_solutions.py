#!/usr/bin/env python3
"""
Script to refactor Advent of Code solution files to use aoc_helpers.py
and reference aoc-data input files.
"""

import os
import re
from pathlib import Path


def refactor_solution_file(file_path, year, day):
    """
    Refactors a single solution file to use aoc_helpers and aoc-data.

    Args:
        file_path: Path to the solution file
        year: Year of the solution (e.g., "2016")
        day: Day of the solution (e.g., "1", "2", etc.)
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Determine if this is solution1 or solution2
    part = "1" if "solution1" in str(file_path) else "2"

    # Check if already refactored
    if 'aoc_helpers' in content and 'aoc-data' in content:
        print(f"  Already refactored: {file_path}")
        return False

    # Build the new imports section
    new_imports = f"""import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/{year}/{day}/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
"""

    # Remove old import statements and file opening code
    lines = content.split('\n')
    new_lines = []
    skip_next = False
    imports_added = False

    for i, line in enumerate(lines):
        # Skip empty lines at the beginning
        if not imports_added and not line.strip() and i < 10:
            continue

        # Skip old file opening patterns
        if re.search(r'\bopen\s*\(\s*["\']input\.txt["\']', line):
            # Add new imports before the file open statement if not added yet
            if not imports_added:
                new_lines.append(new_imports)
                imports_added = True
            continue

        # Replace old print_solution/printSolution with AoCUtils.print_solution
        if 'print_solution' in line.lower() or 'printsolution' in line.lower():
            # Don't skip the function definition itself
            if 'def print_solution' in line.lower() or 'def printSolution' in line.lower():
                continue
            # Replace the call
            line = re.sub(r'\bprint_solution\s*\(', 'AoCUtils.print_solution(' + part + ', ', line)
            line = re.sub(r'\bprintSolution\s*\(', 'AoCUtils.print_solution(' + part + ', ', line)

        # Replace file.read patterns with AoCInput
        if 'file.read' in line or 'f.read' in line:
            if not imports_added:
                new_lines.append(new_imports)
                imports_added = True
            # This needs manual handling, skip for now

        new_lines.append(line)

    # If imports weren't added yet, add them at the beginning
    if not imports_added:
        final_content = new_imports + '\n' + '\n'.join(new_lines)
    else:
        final_content = '\n'.join(new_lines)

    # Write the refactored content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

    print(f"  Refactored: {file_path}")
    return True


def refactor_year(year):
    """
    Refactors all solution files for a given year.

    Args:
        year: Year to refactor (e.g., "2016")
    """
    base_path = Path(f"python/{year}")

    if not base_path.exists():
        print(f"Directory not found: {base_path}")
        return

    print(f"\nRefactoring {year} solutions...")

    # Process each day
    for day in range(1, 26):
        day_str = str(day).zfill(2)
        day_path = base_path / day_str

        if not day_path.exists():
            continue

        print(f"\nDay {day}:")

        # Refactor solution1.py
        solution1 = day_path / "solution1.py"
        if solution1.exists():
            refactor_solution_file(solution1, year, str(day))

        # Refactor solution2.py
        solution2 = day_path / "solution2.py"
        if solution2.exists():
            refactor_solution_file(solution2, year, str(day))


def main():
    """Main function to run the refactoring."""
    # Refactor 2016
    refactor_year("2016")

    # Refactor 2017
    refactor_year("2017")

    print("\n✓ Refactoring complete!")


if __name__ == "__main__":
    main()
