import math
from collections import defaultdict
from functools import lru_cache


def printSolution(x):
    print(f"The solution is {x}")


def createBurrow(filename):
    crabs = defaultdict(list)
    file = open(filename, 'r')
    for y, line in enumerate(file.readlines()):
        for x, pos in enumerate(line.rstrip('\n')):
            if pos != '#' and pos != ' ':
                if pos.isalpha():
                    if pos == 'A':
                        crabs[x].append(0)
                    elif pos == 'B':
                        crabs[x].append(1)
                    elif pos == 'C':
                        crabs[x].append(2)
                    elif pos == 'D':
                        crabs[x].append(3)

    result = []
    for c in range(3, 10, 2):
        result.append(tuple(crabs[c]))
    hallway = [None] * 7
    return tuple(result), tuple(hallway)


def moveIn(state, size):
    rooms, hallway = state

    for idx, crab in enumerate(hallway):
        if crab is None:
            continue
        
        home = rooms[crab]
        occupants = [c for c in home if c != crab]
        if len(occupants):
            continue

        move_cost = costToMove(state, crab, idx, size, True)
        if move_cost == math.inf:
            continue
            
        new_rooms = rooms[:crab] + ((crab,) + home,) + rooms[crab + 1:]
        new_hallway = hallway[:idx] + (None,) + hallway[idx + 1:]
        yield move_cost, (new_rooms, new_hallway)


def moveOut(state, size):
    rooms, hallway = state
    for idx_r, room in enumerate(rooms):
        if len(room) == 0:
            continue
        at_home = [c == idx_r for c in room]
        if all(at_home):
            continue

        for idx_h in range(len(hallway)):
            move_cost = costToMove(state, idx_r, idx_h, size, False)
            if move_cost == math.inf:
                continue

            new_rooms = rooms[:idx_r] + (room[1:],) + rooms[idx_r + 1:]
            new_hallway = hallway[:idx_h] + (room[0],) + hallway[idx_h + 1:]
            yield move_cost, (new_rooms, new_hallway)


def costToMove(state, r, h, size, moving_in=False):
    rooms, hallway = state
    rh_distance = (
        (2, 1, 1, 3, 5, 7, 8),
        (4, 3, 1, 1, 3, 5, 6),
        (6, 5, 3, 1, 1, 3, 4),
        (8, 7, 5, 3, 1, 1, 2),
    )
    if r + 1 < h:
        start = r + 2
        end = h + (not moving_in)
    else:
        start = h + moving_in
        end = r + 2

    if any(x is not None for x in hallway[start:end]):
        return math.inf

    crab = hallway[h] if moving_in else rooms[r][0]

    return 10**crab * (rh_distance[r][h] + (moving_in + size - len(rooms[r])))


def possible_moves(state, size):
    yield from moveIn(state, size)
    yield from moveOut(state, size)


def done(state, size):
    rooms, _ = state
    for r, room in enumerate(rooms):
        if len(room) != size or any(crab != r for crab in room):
            return False
    return True


@lru_cache(maxsize=None)
def solve(state, size):
    if done(state, size):
        return 0

    best = math.inf

    for cost, next_state in possible_moves(state, size):
        cost += solve(next_state, size)
        if cost < best:
            best = cost

    return best


def main():

    start_state = createBurrow('input2.txt')
    min_cost = solve(start_state, len(start_state[0][0]))

    printSolution(min_cost)

if __name__ == "__main__":
    main()
