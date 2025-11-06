"""
Advent of Code 2018 - Day 15: Beverage Bandits
https://adventofcode.com/2018/day/15

Having perfected their hot chocolate, the Elves have a new problem: the Goblins that live in
these caves will do anything to steal it. Looks like they're here for a fight.

This solution simulates combat between Elves and Goblins on a grid, with turn-based movement
and attacking mechanics.

Part 2 modifies the combat simulation to find the minimum attack power required for Elves to win
without any casualties.

"""
import os
import sys
from collections import defaultdict, deque
from functools import lru_cache

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2018/15/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))
from aoc_helpers import AoCUtils


def clear_screen():
    """Clear the console screen for better readability during simulation."""
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For macOS and Linux
    else:
        os.system('clear')

def createGameboard(filename):
    """Parse the input file and create the game board with initial unit positions."""
    board = set()
    elves = defaultdict(int)
    goblins = defaultdict(int)

    file = open(filename, 'r')
    for y, row in enumerate(file.readlines()):
        for x, char in enumerate(row.strip('\n')):
            if char == '#':
                continue
            if char == 'E':
                elves[(x, y)] = 200
            elif char == 'G':
                goblins[(x, y)] = 200
            board.add((x, y))

    return (tuple(board), (elves, goblins))

@lru_cache(maxsize=None)
def getTargets(positions, game):
    """Find all possible target positions adjacent to enemy units."""
    board, players = game
    possible = set()
    for p in positions:
        # Check all four cardinal directions
        for offset in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            target = (p[0] + offset[0], p[1] + offset[1])
            if target in board:
                possible.add(target)
    return tuple(possible)

def BFSTarget(position, targets, game):
    """
    Iterative breadth-first search to find the shortest path to a target position.
    Returns the first step to take towards the nearest target.
    """
    board, players = game
    occupied = set(players[0]) | set(players[1])

    if position in targets:
        return None  # Already at target

    # BFS using a queue: (current_pos, first_step)
    queue = deque()
    visited = {position}

    # Initialize queue with adjacent positions
    for offset in [(0, -1), (-1, 0), (1, 0), (0, 1)]:  # Reading order
        next_pos = (position[0] + offset[0], position[1] + offset[1])
        if next_pos in board and next_pos not in occupied:
            queue.append((next_pos, next_pos))
            visited.add(next_pos)

    # Track targets found at the current distance
    found_targets = []
    current_level_size = len(queue)

    while queue:
        current_pos, first_step = queue.popleft()
        current_level_size -= 1

        # Check if we reached a target
        if current_pos in targets:
            found_targets.append((current_pos, first_step))
            # Continue processing this level to find all equidistant targets
            if current_level_size == 0 and found_targets:
                break
            continue

        # If we finished this level and found targets, stop
        if current_level_size == 0 and found_targets:
            break

        # Explore neighbors in reading order
        for offset in [(0, -1), (-1, 0), (1, 0), (0, 1)]:
            next_pos = (current_pos[0] + offset[0], current_pos[1] + offset[1])
            if next_pos not in visited and next_pos in board and next_pos not in occupied:
                visited.add(next_pos)
                queue.append((next_pos, first_step))

        # Mark end of current level
        if current_level_size == 0:
            current_level_size = len(queue)

    if not found_targets:
        return None

    # Sort targets by reading order (y, then x), then by first step
    found_targets.sort(key=lambda x: (x[0][1], x[0][0], x[1][1], x[1][0]))
    return found_targets[0][1]

@lru_cache(maxsize=None)
def findPath(position, game):
    """
    Find the next move for a unit at the given position.
    Returns the position to move to, or None if no valid path exists.
    """
    board, players = game
    # Determine which team this unit belongs to
    if position in players[0]:
        enemy = players[1]
    else:
        enemy = players[0]

    targets = getTargets(enemy, game)
    if not targets:
        return None

    next_step = BFSTarget(position, targets, game)
    return next_step if next_step else position


def printGameboard(game):
    """Display the current state of the game board for debugging."""
    board, players = game
    elves, goblins = players
    max_x = max([x[0] for x in board])
    max_y = max([x[1] for x in board])
    for y in range(max_y + 2):
        row = ''
        fighters = ''
        for x in range(max_x + 2):
            if (x, y) in goblins.keys():
                row += 'G'
                fighters += f"G({goblins[(x,y)]}) "
            elif (x, y) in elves.keys():
                row += 'E'
                fighters += f"E({elves[(x,y)]}) "
            elif (x, y) in board:
                row += '.'
            else:
                row += '#'
        print(row, fighters)


def simulate_game(game, elf_attack_power=3):
    """Simulate the game until one side wins."""
    # This function is not used in the current solution but can be implemented
    # for further enhancements, such as varying elf attack power.
    round = 0
    fighting = True
    while fighting:
        board, players = game
        elves, goblins = players
        # Process all fighters in reading order
        fighters = list(goblins.keys()) + list(elves.keys())
        fighters.sort(key=lambda x: (x[1], x[0]))

        for f in fighters:
            # Skip if this fighter was already killed this round
            if f not in goblins.keys() and f not in elves.keys():
                continue
            is_goblin = f in goblins.keys()
            # Find and execute movement
            move = findPath(f, (board, (tuple(elves.keys()), tuple(goblins.keys()))))
            if f != move and move is not None:
                # Move the unit to the new position
                if is_goblin:
                    goblins[move] = goblins.pop(f)
                    f = move
                else:
                    elves[move] = elves.pop(f)
                    f = move
            # Check if unit can attack after moving
            move = findPath(f, (board, (tuple(elves.keys()), tuple(goblins.keys()))))
            if f != move and move is not None:
                continue
            # Define attack order (reading order: up, left, right, down)
            fight_order = [
                (f[0], f[1] - 1),
                (f[0] - 1, f[1]),
                (f[0] + 1, f[1]),
                (f[0], f[1] + 1),
                ]
            # Execute attack if enemies are in range
            if is_goblin:
                # Goblins attack elves
                targets = [(v, k) for k, v in elves.items() if k in fight_order]
                if len(targets) == 0:
                    continue
                # Sort by HP, then position (reading order)
                targets.sort(key=lambda x: (x[0], x[1][1], x[1][0]))
                fight = targets[0][1]
                elves[fight] -= 3
                if elves[fight] < 0:
                    elves.pop(fight)
            else:
                # Elves attack goblins
                targets = [(v, k) for k, v in goblins.items() if k in fight_order]
                if len(targets) == 0:
                    continue
                targets.sort(key=lambda x: (x[0], x[1][1], x[1][0]))
                fight = targets[0][1]
                goblins[fight] -= elf_attack_power
                if goblins[fight] < 0:
                    goblins.pop(fight)

            game = (board, (elves, goblins))

        # Check if combat is over (one side eliminated)
        if len(goblins.keys()) == 0 or len(elves.keys()) == 0:
            return round, elves, goblins

        round += 1

def main():
    """Main simulation loop for the combat."""
    game = createGameboard(INPUT_FILE)

    # count the number of elves to ensure none die
    elf_count = len(game[1][0])

    elf_strength = 3
    while True:
        round, elves, goblins = simulate_game(game, elf_attack_power=elf_strength)
        #print(f"With elf attack power {elf_strength}, outcome after {round} rounds: "
        #      f"{len(elves)} elves and {len(goblins)} goblins remain.")
        if len(elves) == elf_count:
            break
        game = createGameboard(INPUT_FILE)
        elf_strength += 1


    # Calculate outcome: rounds * total remaining HP
    AoCUtils.print_solution(2, round * (sum(goblins.values()) + sum(elves.values())))


if __name__ == "__main__":
    main()
