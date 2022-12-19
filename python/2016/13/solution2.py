
from queue import Queue

def printSolution(x):
    print(f"The solution is {x}")

def isOpen(grid_loc, seed):
    x, y = grid_loc
    value = x*x + 3*x + 2*x*y + y + y*y + seed
    return bin(value).count("1") % 2 == 0

def findPaths(state, seed):
    x, y = state[0]
    move = state[1]
    paths = []

    if move > 50:
        return paths

    for loc in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
        if min(loc) < 0:
            continue
        if isOpen(loc, seed):
            paths.append((loc, move+1))
    return paths

def main():
    
    problem = {
        'seed': 1358,
        'start': (1, 1)
    }

    active = problem

    loc_seen = list()
    loc_to_evaluate = Queue()

    move = 0
    loc_to_evaluate.put((active['start'], move))

    searching = True
    while not loc_to_evaluate.empty():
        state = loc_to_evaluate.get()
        loc = state[0]
        if loc in loc_seen:
            continue
        loc_seen.append(loc)

        new_states = findPaths(state, active['seed'])
        for state in new_states:
            if state[0] in loc_seen or state[1] > 50:
                continue
            loc_to_evaluate.put(state)

    printSolution(len(loc_seen))




if __name__ == "__main__":
    main()