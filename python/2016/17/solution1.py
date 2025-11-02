import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2016/17/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils

import copy
from hashlib import md5
from queue import PriorityQueue
def AoCUtils.print_solution(1, x):
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
    path_queue = PriorityQueue()

    path_queue.put((len(path), [path, copy.copy(current_room)]))

    seeking = True

    while seeking:
        _, current = path_queue.get()
        path, room = current
        possible_paths = getPaths(salt+path)
        for p in possible_paths:
            new_room = tuple(a + b for a,b in zip(room, movement[p]))
            new_path = path + p
            if new_room == vault_room:
                seeking = False
                AoCUtils.print_solution(1, new_path)
                break
            if isValidRoom(new_room, dimensions):
                path_queue.put((len(new_path), [new_path, copy.copy(new_room)]))






if __name__ == "__main__":
    main()