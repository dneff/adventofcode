from collections import defaultdict

def printSolution(x):
    print(f"The solution is {x}")


def createGameboard(filename):
    board = set()
    elves = set()
    goblins = set()

    file = open(filename, 'r')
    for y, row in enumerate(file.readlines()):
        for x, char in enumerate(row.strip('\n')):
            if char == '#':
                continue
            if char == 'E':
                elves.add((x, y))
            elif char == 'G':
                goblins.add((x, y))
            board.add((x, y))

    return (board, (elves, goblins))

def getTargets(positions, game):
    board, players = game
    possible = set()
    for p in positions:
        for offset in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            target = (p[0] + offset[0], p[1] + offset[1])
            if target in board:
                possible.add(target)
    return possible


def BFSTarget(position, targets, game, distance=0, seen=list()):
    board, players = game
    occupied = players[0] | players[1]
    distance += 1
    found = list()
    next_paths = set()

    if position in targets:
        found.append(seen[:] + [position])
        return distance, found

    for offset in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_path = (position[0] + offset[0], position[1] + offset[1])
        if new_path in seen:
            continue
        elif new_path in targets:
            found_path = seen[:] + [new_path]
            found.append(found_path)
        else:
            if new_path in board and new_path not in occupied:
                next_paths.add(new_path)

    if len(found) > 0:
        return distance, found

    results = defaultdict(list)
    for path in next_paths:
        new_seen = seen[:] + [path]
        k, v = BFSTarget(path, targets, game, distance, new_seen)
        results[k].extend(v)

    if len(results.keys()) > 0:
        return min(results.keys()), results[min(results.keys())]
    else:
        return 10**10, set()


def findPath(position, game):
    board, players = game
    if position in players[0]:
        enemy = players[1]
    else:
        enemy = players[0]

    _, paths = BFSTarget(position, getTargets(enemy, game), game)
    if len(paths) > 0:
        targets = [x[-1] for x in paths]
        targets.sort(key=lambda x: (x[1], x[0]))
        for path in paths:
            if targets[0] in path:
                return path[0]


def main():
    game = createGameboard('test.txt')
    board, players = game
    elves, goblins = players

    for e in elves:
        move = findPath(e, game)
        if e == move:
            print(f"FIGHT: Elf {e} -> goblin target {move}")
        else:
            print(f"MOVE: Elf {e} -> goblin target {move}")
        
    for g in goblins:
        move = findPath(g, game)
        if g == move:
            print(f"FIGHT: Goblin {g} -> elf target {move}")
        else:
            print(f"MOVE: Goblin {g} -> elf target {move}")
 



if __name__ == "__main__":
    main()
