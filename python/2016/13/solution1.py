import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/13/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
from queue import PriorityQueue

def isOpen(grid_loc, seed):
    x, y = grid_loc
    value = x*x + 3*x + 2*x*y + y + y*y + seed
    return bin(value).count("1") % 2 == 0

def findPaths(state, seed):
    x, y = state[0]
    move = state[1]
    paths = []

    for loc in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
        if min(loc) < 0:
            continue
        if isOpen(loc, seed):
            paths.append((loc, move+1))

    return paths

def distanceFromStart(current):
    return abs(current[0] - 1) + abs(current[1] - 1)

def distanceToDestination(current, destination):
    return abs(destination[0] - current[0]) + abs(destination[1] - current[1])

def getScore(loc, destination, move):
    return move + distanceFromStart(loc) + distanceToDestination(loc, destination)

def main():
    
    test = {
        'seed': 10,
        'start': (1, 1),
        'destination': (7,4)
    }

    problem = {
        'seed': 1358,
        'start': (1, 1),
        'destination': (31,39)
    }

    active = problem

    loc_seen = []
    loc_to_evaluate = PriorityQueue()

    move = 0
    start_score = getScore(active['start'], active['destination'], move)
    loc_to_evaluate.put((start_score, (active['start'], move)))

    searching = True
    while searching:
        _, state = loc_to_evaluate.get()
        loc = state[0]
        if loc in loc_seen:
            continue
        loc_seen.append(loc)

        new_states = findPaths(state, active['seed'])
        for state in new_states:
            if state[0] in loc_seen:
                continue

            if distanceToDestination(state[0], active['destination']) == 0:
                AoCUtils.print_solution(1, state[1])
                searching = False
            
            score = getScore(state[0], active['destination'], state[1])
            loc_to_evaluate.put((score, state))




if __name__ == "__main__":
    main()