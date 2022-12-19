from IntCode import IntCode, InputInterrupt, OutputInterrupt
from collections import deque


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
        

def main():
    with open('input1.txt', 'r') as file:
        program = file.read().strip()

    comp1 = IntCode(program)
    comp1.complete = False

    direction = [1, 4, 2, 3]
    heading = 0

    x, y = 0,0
    positions=[]
    walls=[]
    oxygen=[]

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

    locs = {p:[] for p in set(positions)}
    for loc in locs.keys():
        for d in direction:
            t = newPosition(loc, d)
            if t in locs.keys():
                locs[loc].append((str(d), t))

    result = findPathBFS(locs, oxygen[0], (0, 0))
    print(f"The shortest number of moves from start to oxygen sensor is {len(result)}")

# Part 2 -=-=-=-

    result = findLongestPath(locs, oxygen[0])
    print(f"It will take {result} minutes to flood the space with oxygen.")

if __name__ == "__main__":
    main()