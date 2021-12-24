import copy
import random
from dataclasses import dataclass, field
from typing import Any
from queue import PriorityQueue
from collections import defaultdict


CRAB_GOALS = {}
CRAB_GOALS['A'] = [(3, 2), (3, 3)]
CRAB_GOALS['B'] = [(5, 2), (5, 3)]
CRAB_GOALS['C'] = [(7, 2), (7, 3)]
CRAB_GOALS['D'] = [(9, 2), (9, 3)]

VALID_HALLWAY = [
        (1, 1), (2, 1),
        (4, 1),
        (6, 1),
        (8, 1),
        (10, 1), (11, 1)
    ]


def printSolution(x):
    print(f"The solution is {x}")


def scoreMove(src, dest, crab):
    cost = {
        'A': 1,
        'B': 10,
        'C': 100,
        'D': 1000
    }

    distance = abs(src[0] - dest[0]) + abs(src[1] - dest[1])
    return distance * cost[crab]


def distanceToComplete(crabs):
    distance = 0
    for crab, positions in crabs.items():
        # if both home, then skip
        if positions[0] in CRAB_GOALS[crab] and positions[1] in CRAB_GOALS[crab]:
            continue
        for c in positions:
            if c == CRAB_GOALS[crab][-1]:
                continue
            if c[1] > 1:
                distance += scoreMove(c, (1, 4), crab)
                distance += scoreMove(c, CRAB_GOALS[crab][-1], crab)
            else:
                distance += scoreMove(c, CRAB_GOALS[crab][-1], crab)
    return distance


def createBurrow(filename):
    burrow = set()
    crabs = defaultdict(list)
    file = open(filename, 'r')
    for y, line in enumerate(file.readlines()):
        for x, pos in enumerate(line.rstrip('\n')):
            if pos != '#' and pos != ' ':
                if pos.isalpha():
                    crabs[pos].append((x, y))
                burrow.add((x, y))
    return burrow, crabs


def validPath(src, dest, crabspots):
    # heading to hallway
    src = list(src)
    if src[1] > dest[1]:
        while src[1] > dest[1]:
            src[1] -= 1
            if src in crabspots:
                return False
    path = [(x, 1) for x in range(min(src[0], dest[0]), max(src[0], dest[0]) + 1)]
    for p in path:
        if p in crabspots:
            return False
    if src[1] < dest[1]:
        while src[1] < dest[1]:
            src[1] += 1
            if src in crabspots:
                return False
    return True


def findPossibleStates(state):
    new_states = []
    print(state)
    score, crabs = state
    crab_spots = [c for crab in crabs for c in crab]
    for id, crab in crabs.items():
        for idx, position in enumerate(crab):
            # are we heading to goal?
            if position in VALID_HALLWAY:
                for g in CRAB_GOALS[id]:
                    if validPath(position, g, crab_spots):
                        s = copy.deepcopy(state)
                        s[1][id][idx] = g
                        score = s[0] + scoreMove(position, g, id)
                        new_states.append((score, s[1]))
            else:
                for g in VALID_HALLWAY:
                    if g not in crab_spots:
                        if validPath(position, g, crab_spots):
                            s = copy.deepcopy(state)
                            s[1][id][idx] = g
                            score = s[0] + scoreMove(position, g, id)
                            new_states.append((score, s[1]))
    return new_states



@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)


def main():

    states_seen = []
    states_to_evaluate = PriorityQueue()
    score = 0

    burrow, crabs = createBurrow('test.txt')
    start_distance = distanceToComplete(crabs)

    start_state = (score, crabs)
    states_to_evaluate.put((start_distance, start_state))

    searching = True
    while searching:
        _, crab_state = states_to_evaluate.get()
        if crab_state[1] in states_seen:
            continue
        states_seen.append(crab_state[1])

        new_states = findPossibleStates(crab_state)

        for state in new_states:
            if state[0] in states_seen:
                continue
            if distanceToComplete(state[1]) == 0:
                printSolution(state[0])
                searching = False
            try:
                states_to_evaluate.put((distanceToComplete(state[1]) + random.randrange(5), state))
            except TypeError:
                states_to_evaluate.put((distanceToComplete(state[1]) + random.randrange(2000), state))

if __name__ == "__main__":
    main()
