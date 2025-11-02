# adventofcode
consolidated AoC repo for all work

## Verification Script

Use `verify_solutions.py` to verify solutions against known correct answers stored in the `aoc-data` repository:

```bash
# Verify solutions for a specific year
python3 verify_solutions.py 2015
python3 verify_solutions.py 2016

# Default is 2015
python3 verify_solutions.py
```

The script will:
- Run each solution file for the specified year
- Compare outputs against verified answers in `../aoc-data/YEAR/DAY/solution-{1,2}`
- Report correct, incorrect, and failed solutions
- Display execution times for each solution
