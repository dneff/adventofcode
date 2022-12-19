import copy
from queue import PriorityQueue
from collections import defaultdict
from itertools import combinations

# implementing A* path resolution
# distance = (top floor - floor of item) for all items. If distance == 0, then search is complete

# state rating = distance from start + distance to complete + current move count
# using a priority queue to get best next state to explore


def printSolution(x):
    print(f"The solution is {x}")

def parseItems(sentence):
    items = []
    for i, word in enumerate(sentence.replace(".","").replace(",","") .split()):
        if word in ['microchip', 'generator']:
            item = sentence.split()[i-1].split("-")[0] + "." + word
            items.append(item)
    return items

def createBuilding(filename):
    building = {}
    building['elevator'] = 1
    building['floors'] = 0
    items = defaultdict(lambda: [0] * 2)
    file = open(filename, 'r')
    for floor, sentence in enumerate(file):
        building['floors'] += 1
        for item in parseItems(sentence):
            element, type = item.split('.')
            if type == 'generator':
                position = 1
            else:
                position = 0
            items[element][position] = floor + 1
    # --- additions for part 2
    items['elerium'] = [1,1]
    items['dilithium'] = [1,1]

    return sorted([list(x) for x in items.values()]), building['floors'], building['elevator']

def itemsValid(items):
    # are microchips exposed?
    generator_locations = [x[1] for x in items]
    for chip, generator in items:
        if chip == generator:
            continue
        if chip in generator_locations:
            return False
    return True

def lowestUsedFloor(building):
    for f in range(1, building['floors'] + 1):
        if len(building[f]) > 0:
            return f    

def distanceToComplete(items, floors):
    values = []
    for pair in items:
        values.extend(pair)
    distance = floors * len(values) - sum(values)
    return distance

def getScore(state, starting_distance, floors):
    score = 0
    #score += starting_distance
    score += distanceToComplete(state[0], floors)
    score += state[-1]

    return score

def findPossibleStates(state, floors):
    states = []
    items, elevator, moves = state
    values = []
    for pair in items:
        values.extend(list(pair))

    min_floor = min(values)

    scoped_items = []

    for pair_idx, pair in enumerate(items):
        for part_idx, part in enumerate(pair):
            if part == elevator:
                scoped_items.append([pair_idx, part_idx])

    combos = []
    combos.extend(combinations(scoped_items, 1))
    combos.extend(combinations(scoped_items, 2))

    if elevator < floors:
        for combo in combos:
            new_items = copy.deepcopy(items)
            for delta in combo:
                new_items[delta[0]][delta[1]] = elevator + 1
            new_items.sort()
            if itemsValid(new_items):
                states.append((new_items, elevator + 1, moves + 1))

    if elevator > min_floor:
        for combo in combos:
            new_items = copy.deepcopy(items)
            for delta in combo:
                new_items[delta[0]][delta[1]] = elevator - 1
            new_items.sort()
            if itemsValid(new_items):
                states.append((new_items, elevator - 1, moves + 1))
    return states



def main():
    states_seen = list()
    states_to_evaluate = PriorityQueue()
    moves = 0

    items, floors, elevator = createBuilding('input.txt')
    start_distance = distanceToComplete(items, floors)
    
    start_state = (items, elevator, moves)
    states_to_evaluate.put((getScore(start_state, start_distance, floors), start_state))

    searching = True
    while searching:
        moves += 1
        _, state = states_to_evaluate.get()
        if ((state[0], state[1])) in states_seen:
            continue
        states_seen.append((state[0], state[1]))

        new_states = findPossibleStates(state, floors)
        
        for state in new_states:
            if (state[0], state[1]) in states_seen:
                continue
            if distanceToComplete(state[0], floors) == 0:
                printSolution(state[-1])
                searching = False

            states_to_evaluate.put((getScore(state, start_distance, floors), state))

if __name__ == "__main__":
    main()