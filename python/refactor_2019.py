#!/usr/bin/env python3
"""
Script to refactor 2019 Advent of Code solution files to use aoc_helpers.py
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
        year: Year of the solution (e.g., "2019")
        day: Day of the solution (e.g., "1", "2", etc.)
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Determine if this is solution1, solution2, or solution
    filename = os.path.basename(file_path)
    if "solution1" in filename:
        part = "1"
    elif "solution2" in filename:
        part = "2"
    else:
        part = "1"  # Default for solution.py files

    # Check if already refactored
    if 'aoc_helpers' in content and 'aoc-data' in content:
        print(f"  Already refactored: {file_path}")
        return False

    # Skip IntCode.py, Point.py, and other helper files
    if filename in ['IntCode.py', 'Point.py', 'refactor.py', 'tester_IntCode.py']:
        print(f"  Skipping helper file: {file_path}")
        return False

    # Build the new imports section
    imports_to_add = []

    # Check for existing imports we want to preserve
    lines = content.split('\n')
    existing_imports = []
    for line in lines:
        if line.strip().startswith('from itertools') or \
           line.strip().startswith('import itertools') or \
           line.strip().startswith('from collections') or \
           line.strip().startswith('import collections') or \
           line.strip().startswith('import math') or \
           line.strip().startswith('import re') or \
           line.strip().startswith('import sys') and 'SCRIPT_DIR' not in content:
            existing_imports.append(line)

    # Build header
    header = ["import os", "import sys", ""]
    if existing_imports:
        header.extend(existing_imports)
        header.append("")

    header.extend([
        "# Path setup",
        "SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))",
        "sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))",
        "",
        "from aoc_helpers import AoCInput, AoCUtils  # noqa: E402",
        "",
        "# Input file path",
        f"INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/{year}/{day}/input')",
        ""
    ])

    new_header = '\n'.join(header)

    # Remove old imports and file operations
    new_lines = []
    skip_line = False
    found_def_or_class = False

    for i, line in enumerate(lines):
        # Skip empty lines at the beginning
        if not found_def_or_class and not line.strip():
            continue

        # Skip old imports that are now in header
        if re.match(r'^\s*(import|from)\s+(math|itertools|collections|re)\b', line):
            continue

        # Skip file operations
        if re.search(r'\bopen\s*\(\s*["\']input1?\.txt["\']', line) or \
           re.search(r'with\s+open\s*\(\s*["\']input1?\.txt["\']', line):
            # Skip the with/open line
            if 'with open' in line:
                skip_line = True
            continue

        if skip_line and ':' in line:
            skip_line = False
            continue

        # Found first function or class - we're past the import section
        if re.match(r'^\s*def\s+\w+|^\s*class\s+\w+', line):
            found_def_or_class = True

        # Replace file.read() and similar patterns
        if 'file.read' in line:
            line = re.sub(r'file\.read\(\)', 'AoCInput.read_file(INPUT_FILE)', line)
        if 'file.readlines' in line:
            line = re.sub(r'file\.readlines\(\)', 'AoCInput.read_lines(INPUT_FILE)', line)

        new_lines.append(line)

    # Combine header and code
    final_content = new_header + '\n' + '\n'.join(new_lines)

    # Replace print statements with returns in main/solve functions
    final_content = re.sub(
        r'def main\(\):',
        f'def solve_part{part}():',
        final_content
    )

    # Replace if __name__ == "__main__": main() pattern
    final_content = re.sub(
        r'if __name__ == "__main__":\s+main\(\)',
        f'answer = solve_part{part}()\nAoCUtils.print_solution({part}, answer)',
        final_content
    )

    # Write the refactored content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

    print(f"  Refactored: {file_path}")
    return True


def main():
    """Main function to run the refactoring."""
    base_dir = Path(__file__).parent / "2019"

    print("Refactoring 2019 solutions...")

    # Process each day
    for day in range(9, 20):  # Days 09-19
        day_str = str(day).zfill(2)
        day_path = base_dir / day_str

        if not day_path.exists():
            continue

        print(f"\nDay {day}:")

        # Refactor solution.py (common pattern in 2019)
        solution = day_path / "solution.py"
        if solution.exists():
            refactor_solution_file(solution, "2019", str(day))

        # Refactor solution1.py
        solution1 = day_path / "solution1.py"
        if solution1.exists():
            refactor_solution_file(solution1, "2019", str(day))

        # Refactor solution2.py
        solution2 = day_path / "solution2.py"
        if solution2.exists():
            refactor_solution_file(solution2, "2019", str(day))

    print("\n✓ Refactoring complete!")


if __name__ == "__main__":
    main()
