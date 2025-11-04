"""
Advent of Code 2018 - Day 15: Beverage Bandits
https://adventofcode.com/2018/day/15

Having perfected their hot chocolate, the Elves have a new problem: the Goblins that live in
these caves will do anything to steal it. Looks like they're here for a fight.

This solution simulates combat between Elves and Goblins on a grid, with turn-based movement
and attacking mechanics.
"""
import os
import sys
from collections import defaultdict
from functools import lru_cache

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2018/15/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))
from aoc_helpers import AoCUtils


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

@lru_cache(maxsize=None)
def BFSTarget(position, targets, game, distance=0, seen=list()):
    """
    Breadth-first search to find the shortest path to a target position.
    Returns the distance and list of paths found.
    """
    board, players = game
    occupied = set(players[0]) | set(players[1])
    distance += 1
    found = list()
    next_paths = set()

    # Limit search depth for performance
    if distance > 8:
        return 10**10, set()

    if position in targets:
        found.append(seen[:] + [position])
        return distance, found

    for offset in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_path = (position[0] + offset[0], position[1] + offset[1])
        if new_path in seen:
            continue
        elif new_path in targets and new_path not in occupied:
            found_path = list(seen)[:] + [new_path]
            found.append(found_path)
        elif new_path in board and new_path not in occupied:
            next_paths.add(new_path)

    if len(found) > 0:
        return distance, found

    if len(next_paths) == 0:
        return 10**10, set()

    results = defaultdict(list)
    for path in next_paths:
        new_seen = list(seen)[:] + [path]
        k, v = BFSTarget(path, targets, (board, players), distance, tuple(new_seen))
        results[k].extend(v)

    if len(results.keys()) > 0:
        return min(results.keys()), results[min(results.keys())]
    else:
        return 10**10, set()

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
    _, paths = BFSTarget(position, getTargets(enemy, game), game)
    if len(paths) > 0:
        # Sort targets in reading order (top-to-bottom, left-to-right)
        targets = [x[0] for x in paths]
        targets.sort(key=lambda x: (x[1], x[0]))
        for path in paths:
            if targets[0] in path:
                return path[0]


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


def main():
    """Main simulation loop for the combat."""
    game = createGameboard(INPUT_FILE)
    print(f"INITIAL STATE ---------------")
    printGameboard(game)
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
                targets.sort()
                fight = targets[0][1]
                goblins[fight] -= 3
                if goblins[fight] < 0:
                    goblins.pop(fight)

            game = (board, (elves, goblins))

        print(f"After {round} rounds - E: {sum(elves.values())} G: {sum(goblins.values())}")
        printGameboard(game)
        # Check if combat is over (one side eliminated)
        if len(goblins.keys()) == 0 or len(elves.keys()) == 0:
            fighting = False
            continue

        round += 1

    print(f"ends after {round} rounds")
    # Calculate outcome: rounds * total remaining HP
    AoCUtils.print_solution(1, round * (sum(goblins.values()) + sum(elves.values())))




if __name__ == "__main__":
    main()
