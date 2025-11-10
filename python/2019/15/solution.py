import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/15/input')

from IntCode import IntCode, InputInterrupt, OutputInterrupt  # noqa: E402
from collections import deque  # noqa: E402


def newPosition(pos, dir):
    delta = {
        1: (0, 1),
        2: (0, -1),
        4: (1, 0),
        3: (-1, 0)
    }

    return (pos[0] + delta[dir][0], pos[1] + delta[dir][1])


def findPathBFS(locations, start, end):
    queue = deque([("", start)])
    visited = set()

    while queue:
        path, current = queue.popleft()
        if current == end:
            return path
        if current in visited:
            continue
        visited.add(current)
        for direction, neighbor in locations[current]:
            queue.append((path + direction, neighbor))
    return "nothin"


def findLongestPath(locations, start):
    path_lengths = []
    for loc in locations:
        if start == loc:
            continue
        path_lengths.append(len(findPathBFS(locations, start, loc)))
    return max(path_lengths)


def solve_parts():
    program = AoCInput.read_file(INPUT_FILE).strip()

    comp1 = IntCode(program)
    comp1.complete = False

    direction = [1, 4, 2, 3]
    heading = 0

    x, y = 0, 0
    positions = []
    walls = []
    oxygen = []

    positions.append((x, y))

    while True:
        try:
            comp1.run()
        except(InputInterrupt):
            comp1.input.clear()
            comp1.push(direction[heading])
        except(OutputInterrupt):
            move_status = comp1.pop()
            if move_status == 0:
                walls.append(newPosition((x, y), direction[heading]))
                heading = (heading + 1) % 4
            elif move_status == 1:
                x, y = newPosition((x, y), direction[heading])
                positions.append((x, y))
                heading = (heading - 1) % 4
            elif move_status == 2:
                x, y = newPosition((x, y), direction[heading])
                oxygen.append((x, y))
                positions.append((x, y))

        if (x, y) == (0, 0) and len(oxygen) > 0:
            break

    locs = {p: [] for p in set(positions)}
    for loc in locs.keys():
        for d in direction:
            t = newPosition(loc, d)
            if t in locs.keys():
                locs[loc].append((str(d), t))

    result1 = findPathBFS(locs, oxygen[0], (0, 0))
    result2 = findLongestPath(locs, oxygen[0])

    return len(result1), result2


answer1, answer2 = solve_parts()
AoCUtils.print_solution(1, f"The shortest number of moves from start to oxygen sensor is {answer1}")
AoCUtils.print_solution(2, f"It will take {answer2} minutes to flood the space with oxygen")
