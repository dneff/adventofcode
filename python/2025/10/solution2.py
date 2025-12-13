"""
Advent of Code 2025 - Day 10: Factory
https://adventofcode.com/2025/day/10

The input describes one machine per line. Each line contains a single indicator 
light diagram in [square brackets], one or more button wiring schematics in 
(parentheses), and joltage requirements in {curly braces}.

Part 2
All of the machines are starting to come online! Now, it's time to worry about 
the joltage requirements.

Each machine needs to be configured to exactly the specified joltage levels to 
function properly. Below the buttons on each machine is a big lever that you can 
use to switch the buttons from configuring the indicator lights to increasing 
the joltage levels. (Ignore the indicator light diagrams.)

The machines each have a set of numeric counters tracking its joltage levels, one 
counter per joltage requirement. The counters are all initially set to zero.

So, joltage requirements like {3,5,4,7} mean that the machine has four counters 
which are initially 0 and that the goal is to simultaneously configure the first 
counter to be 3, the second counter to be 5, the third to be 4, and the fourth 
to be 7.

The button wiring schematics are still relevant: in this new joltage configuration 
mode, each button now indicates which counters it affects, where 0 means the first 
counter, 1 means the second counter, and so on. When you push a button, each 
listed counter is increased by 1.

So, a button wiring schematic like (1,3) means that each time you push that 
button, the second and fourth counters would each increase by 1. If the current 
joltage levels were {0,1,2,3}, pushing the button would change them to be {0,2,2,4}.

Analyze each machine's joltage requirements and button wiring schematics. What 
is the fewest button presses required to correctly configure the joltage level 
counters on all of the machines?


Strategy:
For each machine, we can represent the joltage counters and button connections
as tuples of integers. The target configuration is derived from the joltage
requirements, and each button's effect is represented as a tuple indicating
which counters it increments. We can use tuple addition to determine the minimum
number of button presses needed to achieve the target configuration.

This is a breadth-first search (BFS) problem in the space of button press
combinations. We will explore all possible configurations by pressing buttons and
track the minimum presses needed to reach the target configuration. We stop when a path
repeats or when we reach the target configuration.

Optimization Strategy:
The initial BFS approach is far too slow for larger configurations due to exponential
state space growth. This problem is actually an Integer Linear Programming (ILP)
problem where we want to find non-negative integer button press counts that minimize
the total presses while satisfying the joltage requirements.

Optimizations implemented:
1. Integer Linear Programming (ILP): Uses scipy.optimize.milp to solve the problem
   mathematically in polynomial time instead of exponential search. This reduces
   complexity from O(product of target values) to polynomial in the problem size.
2. Parallel Processing: Uses multiprocessing to solve multiple machines concurrently
   across CPU cores, providing linear speedup with number of cores.
3. A* Fallback: If scipy is unavailable, falls back to A* search with improved
   heuristic and iteration limits to prevent infinite loops.

Interesting bug:
During development, I encountered a bug where the ILP solver returned non-integer
solutions due to floating-point precision issues. Summing floats truncated the decimal
part, leading to incorrect button press counts. To fix this, the values are rounded
before summation, and a tolerance check is added to ensure all button press counts
are effectively integers.
"""

import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "../../"))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402
from multiprocessing import Pool
import heapq

# Try to import scipy for ILP solver (much faster)
try:
    from scipy.optimize import milp, LinearConstraint, Bounds
    import numpy as np
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    print("Warning: scipy not available, using slower A* search")

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, "../../../../aoc-data/2025/10/input")
machines = AoCInput.read_lines(INPUT_FILE)

def parse_machine(line):
    """Parse a machine line into its components."""
    target_joltage = [int(x.strip()) for x in line[line.index('{')+1:line.index('}')].strip().split(',')]
    button_schematics = line[line.index('] (')+3:line.index(') {')].strip().split(') (')
    button_effects = [tuple(int(x.strip()) for x in schematic.split(',')) for schematic in button_schematics]
    return tuple(target_joltage), button_effects

def solve_with_ilp(target_config, button_effects):
    """
    Solve using Integer Linear Programming (ILP).
    This is MUCH faster than search for large problems.

    We want to find non-negative integers x1, x2, ..., xn (button press counts)
    that minimize sum(xi) such that pressing each button xi times achieves target.
    """
    if not SCIPY_AVAILABLE:
        return solve_with_astar(target_config, button_effects)

    num_counters = len(target_config)
    num_buttons = len(button_effects)

    # Build constraint matrix A where A[i,j] = 1 if button j affects counter i
    A = np.zeros((num_counters, num_buttons), dtype=int)
    for button_idx, button_effect in enumerate(button_effects):
        for counter_idx in button_effect:
            A[counter_idx, button_idx] += 1

    # Objective: minimize sum of all button presses
    c = np.ones(num_buttons)

    # Equality constraint: A * x = target_config
    constraints = LinearConstraint(A, lb=target_config, ub=target_config)

    # Bounds: x >= 0 for all buttons (non-negative integer)
    bounds = Bounds(lb=0, ub=np.inf)

    # Solve ILP
    # Use integrality constraint - all variables must be integers
    integrality = np.ones(num_buttons)  # 1 = integer constraint

    result = milp(c=c, constraints=constraints, bounds=bounds, integrality=integrality)

    if result.success:
        # Verify the solution is correct
        achieved = A @ result.x
        if not np.allclose(achieved, target_config, atol=0.1):
            print(f"  ILP solution verification FAILED!")
            print(f"    Target: {target_config}")
            print(f"    Achieved: {achieved}")
            print(f"    Button presses: {result.x}")
            print(f"  Falling back to A*")
            return solve_with_astar(target_config, button_effects)

        # Verify all button presses are non-negative integers
        if not all(x >= -0.01 and abs(x - round(x)) < 0.01 for x in result.x):
            print(f"  ILP returned non-integer solution: {result.x}")
            print(f"  Falling back to A*")
            return solve_with_astar(target_config, button_effects)

        # Return total button presses
        return int(np.sum(np.round(result.x)))
    else:
        # Fallback to A* if ILP fails
        print(f"  ILP failed: {result.message}, falling back to A*")
        return solve_with_astar(target_config, button_effects)

def solve_with_astar(target_config, button_effects):
    """
    Use A* search to find minimum button presses needed.
    Fallback when ILP is not available or fails.
    """
    start = (0,) * len(target_config)

    # Improved heuristic: for each counter, estimate minimum presses needed
    def heuristic(config):
        max_remaining = 0
        for i in range(len(config)):
            remaining = target_config[i] - config[i]
            if remaining > 0:
                # Count how many buttons can affect this counter
                buttons_for_counter = sum(1 for btn in button_effects if i in btn)
                if buttons_for_counter > 0:
                    # At minimum, need ceil(remaining / buttons_for_counter) presses
                    min_presses = remaining  # Conservative: assume each button press helps this counter
                    max_remaining = max(max_remaining, min_presses)
        return max_remaining

    # Priority queue: (estimated_total_cost, current_cost, config)
    pq = [(heuristic(start), 0, start)]
    visited = {start: 0}

    iterations = 0
    max_iterations = 10_000_000  # Prevent infinite loops

    while pq and iterations < max_iterations:
        iterations += 1
        est_total, current_cost, current_config = heapq.heappop(pq)

        # If we've reached the target, return the cost
        if current_config == target_config:
            return current_cost

        # Skip if we've found a better path to this state
        if visited.get(current_config, float('inf')) < current_cost:
            continue

        # Try pressing each button
        for button_effect in button_effects:
            new_config = list(current_config)
            for index in button_effect:
                new_config[index] += 1
            new_config = tuple(new_config)

            # Skip if any counter exceeds target (pruning)
            if not all(new_config[i] <= target_config[i] for i in range(len(target_config))):
                continue

            new_cost = current_cost + 1

            # Only explore if this is a better path to this state
            if new_cost < visited.get(new_config, float('inf')):
                visited[new_config] = new_cost
                est_total = new_cost + heuristic(new_config)
                heapq.heappush(pq, (est_total, new_cost, new_config))

    if iterations >= max_iterations:
        print(f"  WARNING: A* hit iteration limit!")
    return None  # No solution found

def solve_machine(args, debug=False):
    """Wrapper for parallel processing."""
    idx, line = args
    try:
        target_config, button_effects = parse_machine(line)
        if debug:
            print(f"[Machine {idx+1}] Target: {target_config}, Buttons: {len(button_effects)}")

        button_presses = solve_with_ilp(target_config, button_effects)

        if button_presses is None:
            print(f"[Machine {idx+1}] ERROR: No solution found!")
            return None
        else:
            if debug:
                print(f"[Machine {idx+1}] ✓ Solution: {button_presses} presses")
            return button_presses
    except Exception as e:
        print(f"[Machine {idx+1}] EXCEPTION: {e}")
        import traceback
        traceback.print_exc()
        return None

# Solve machines in parallel using multiple CPU cores
if __name__ == '__main__':
    import argparse
    from functools import partial

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', help='Run sequentially with verbose output')
    args = parser.parse_args()

    print(f"Solving {len(machines)} machines...")
    print(f"Using {'ILP solver (fast)' if SCIPY_AVAILABLE else 'A* search (slow)'}")

    if args.debug:
        # Sequential execution for debugging with verbose output
        print(f"Running in DEBUG mode (sequential)\n")
        machine_button_presses = [solve_machine((i, line), debug=True) for i, line in enumerate(machines)]
    else:
        # Use multiprocessing to solve machines in parallel (quiet mode)
        num_processes = min(len(machines), os.cpu_count() or 1)
        print(f"Using {num_processes} parallel processes")
        print("Processing...\n")

        # Use partial to pass debug=False to solve_machine
        solve_fn = partial(solve_machine, debug=False)
        with Pool(processes=num_processes) as pool:
            machine_button_presses = pool.map(solve_fn, enumerate(machines))

    # Separate successful and failed results
    valid_results = [x for x in machine_button_presses if x is not None]
    failed_count = len(machines) - len(valid_results)

    if args.debug:
        print(f"\n{'='*60}")
        print(f"Results Summary:")
        print(f"  Total machines: {len(machines)}")
        print(f"  Successful: {len(valid_results)}")
        print(f"  Failed: {failed_count}")

    if failed_count > 0:
        print(f"\n⚠️  WARNING: {failed_count} machines failed to solve!")
        print(f"  Failed machine indices: {[i+1 for i, x in enumerate(machine_button_presses) if x is None]}")

    if len(valid_results) > 0 and args.debug:
        print(f"\n  Total button presses (successful only): {sum(valid_results)}")
        print(f"  Min presses per machine: {min(valid_results)}")
        print(f"  Max presses per machine: {max(valid_results)}")
        print(f"  Average presses per machine: {sum(valid_results) / len(valid_results):.1f}")

    if failed_count > 0:
        print("ERROR: Cannot compute total because some machines failed!")
        print("Please investigate the failed machines.")
        print("Rerun with --debug for more details.")
    else:
        total_button_presses = sum(valid_results)
        AoCUtils.print_solution(2, total_button_presses)