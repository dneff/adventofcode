# adventofcode

Consolidated Advent of Code repository containing solutions in multiple programming languages.

## Repository Structure

This repository follows a multi-language design pattern, organizing solutions by language:

```
adventofcode/
├── python/              # Python solutions and tooling
│   ├── YEAR/DAY/       # Solution files (solution1.py, solution2.py)
│   ├── aoc_helpers.py  # Shared helper library
│   ├── verify_solutions.py    # Verification script
│   └── refactor_solutions.py  # Refactoring utility
├── go/                 # Go solutions and tooling
│   └── 2022/          # Go solutions for 2022
├── CLAUDE.md          # Instructions for Claude Code
└── README.md          # This file
```

**Design Principle**: The root directory contains only documentation and configuration files (*.md, *.txt, *.yaml, etc.). Language-specific code, including utility scripts, resides within language subdirectories.

## Python Solutions

### Verification Script

Use `python/verify_solutions.py` to verify solutions against known correct answers stored in the `aoc-data` repository:

```bash
# Verify all years
python3 python/verify_solutions.py

# Verify solutions for a specific year
python3 python/verify_solutions.py 2015

# Verify a specific day
python3 python/verify_solutions.py 2015 20

# Write missing answers
python3 python/verify_solutions.py 2015 --write-missing
```

The script will:
- Run each solution file for the specified year
- Compare outputs against verified answers in `../aoc-data/YEAR/DAY/solution-{1,2}`
- Report correct, incorrect, and failed solutions
- Display execution times for each solution
