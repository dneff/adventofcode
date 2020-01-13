import queue
import heapq
from functools import lru_cache
from collections import deque, namedtuple, defaultdict
from math import inf

graph = {}

@lru_cache(2**20)
def minSteps(start, to_find, mykeys = frozenset()):
    global graph
    if to_find == 0:
        return 0
    best = inf

    for s in start:
        for k, d in reachableKeys(s, mykeys):
            new_keys = mykeys | {k}
            new_sources = start.replace(s, k)
            dist = d

            dist += minSteps(new_sources, to_find - 1, new_keys)

            if dist < best:
                best = dist

    return best


@lru_cache(2**20)
def reachableKeys(start, mykeys):
    global graph 
    distance = defaultdict(lambda: inf)
    queue = []
    reachable = []

    for node in graph[start]:
        neighbor = node[0]
        weight = node[1]
        queue.append((weight, neighbor))

    heapq.heapify(queue)

    while(queue):
        dist, node = heapq.heappop(queue)

        if node.islower() and node not in mykeys:
            reachable.append((node, dist))
            continue

        if node.lower() not in mykeys:
            continue

        for neighbor, weight in graph[node]:
            new_dist = dist + weight
            if new_dist < distance[neighbor]:
                distance[neighbor] = new_dist
                heapq.heappush(queue, (new_dist, neighbor))

    return reachable

def findAdjacent(graph, deps, start):
    queue = deque()
    visited = {start}
    found = []

    for n in graph[start]:
        queue.append((1, n))

    while queue:
        dist, node = queue.popleft()
        if node not in visited:
            visited.add(node)

            if node in deps.values():
                k = [k for k,v in deps.items() if v == node]
                if k[0] not in ['@','1','2','3','4'] and k[0] not in found:
                    found.append((k[0], dist))
                    continue
    
            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append((dist + 1, neighbor))

    return found


def main():
    global graph
    graph = defaultdict(list)
    deps = {}

    with open('input.txt', 'r') as file:
        maze = [x.strip() for x in file.readlines()]
    y = 0
    for r in maze:
        if r[0] == ';':
            continue
        x = 0
        for c in r:
            if c != "#":
                graph[(x,y)] = []
                if c != '.':
                    deps[c] = (x, y)
            x += 1
        y += 1
    for p in graph.keys():
        for d in [(0, -1),(0, 1),(1, 0),(-1, 0)]:
            test = (p[0] + d[0], p[1] + d[1])
            if test in graph.keys() and test not in graph[p]:
                graph[p].append(test)

    d = {}
    for k, v in deps.items(): 
        d[k] = findAdjacent(graph, deps, v)

    graph = d
    total_keys = sum(node.islower() for node in d)
    min_steps = minSteps('@', total_keys)
    print(f"Solution 1: The minimum steps to get all keys is {min_steps}.")

# Part 2 -=-=-=-
    minSteps.cache_clear()
    reachableKeys.cache_clear()

    graph = defaultdict(list)
    deps = {}

    with open('input2.txt', 'r') as file:
        maze = [x.strip() for x in file.readlines()]
    robot = 1
    y = 0
    for r in maze:
        if r[0] == ';':
            continue
        x = 0
        for c in r:
            if c != "#":
                graph[(x,y)] = []
                if c != '.':
                    if c == '@':
                        deps[str(robot)] = (x,y)
                        robot += 1
                    else:
                        deps[c] = (x, y)
            x += 1
        y += 1
    for p in graph.keys():
        for d in [(0, -1),(0, 1),(1, 0),(-1, 0)]:
            test = (p[0] + d[0], p[1] + d[1])
            if test in graph.keys() and test not in graph[p]:
                graph[p].append(test)

    d = {}
    for k, v in deps.items(): 
        d[k] = findAdjacent(graph, deps, v)

    graph = d
    total_keys = sum(node.islower() for node in d)
    min_steps = minSteps('1234', total_keys)
    print(f"Solution 2: The minimum steps to get all keys is {min_steps}.")


if __name__ == "__main__":
    main()