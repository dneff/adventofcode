import copy
from hashlib import md5
from queue import PriorityQueue


def printSolution(x):
    print(f"The solution is {x}")

def getHash(salted_path):
    result = md5(salted_path.encode())
    return result.hexdigest()

def getPaths(salted_path):
    path_hash = getHash(salted_path)
    door_check = ['b','c','d','e','f']
    is_door = [x in door_check for x in path_hash[:4]]
    directions = ['U','D','L','R']
    return [p for p,d in zip(directions, is_door) if d == True]

def isValidRoom(room, dimensions):
    x,y  = room
    if x <= 0 or x > dimensions[0]:
        return False
    if y <= 0 or y > dimensions[1]:
        return False
    return True


def main():
    movement = {'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R':(1, 0)}

    test1 = 'ihgpwlah' #shortest: DDRRRD, longest: 370
    test2 = 'kglvqrro' #shortest: DDUDRLRRUDRD, longest: 492
    test3 = 'ulqzkmiv' #shortest: DRURDRUDDLLDLUURRDULRLDUUDDDRR, longest: 830

    puzzle = 'ioramepc'

    salt = puzzle

    dimensions = (4, 4)
    vault_room = (4, 4)

    path = ''
    current_room = (1, 1)

    seen_paths = []
    paths_to_vault = set()
    path_queue = PriorityQueue()

    path_queue.put((len(path), [path, copy.copy(current_room)]))

    while not path_queue.empty():
        _, current = path_queue.get()
        path, room = current
        if path in seen_paths:
            continue
        seen_paths.append(path)
        possible_paths = getPaths(salt+path)
        for p in possible_paths:
            new_room = tuple(a + b for a,b in zip(room, movement[p]))
            new_path = path + p
            if new_room == vault_room:
                # paths cannot pass through vault room
                paths_to_vault.add(len(new_path))
                continue
            if isValidRoom(new_room, dimensions):
                path_queue.put((len(new_path), [new_path, copy.copy(new_room)]))

    printSolution(max(paths_to_vault))


if __name__ == "__main__":
    main()