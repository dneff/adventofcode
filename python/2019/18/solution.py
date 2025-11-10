import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path - this puzzle uses two different input files
INPUT_FILE = os.path.join(SCRIPT_DIR, 'input.txt')
INPUT_FILE2 = os.path.join(SCRIPT_DIR, 'input2.txt')

import queue  # noqa: E402
import heapq  # noqa: E402
from functools import lru_cache  # noqa: E402
from collections import deque, namedtuple, defaultdict  # noqa: E402
from math import inf  # noqa: E402

graph = {}


@lru_cache(2**20)
def minSteps(start, to_find, mykeys=frozenset()):
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
                k = [k for k, v in deps.items() if v == node]
                if k[0] not in ['@', '1', '2', '3', '4'] and k[0] not in found:
                    found.append((k[0], dist))
                    continue

            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append((dist + 1, neighbor))

    return found


def solve_part1():
    global graph
    graph = defaultdict(list)
    deps = {}

    lines = AoCInput.read_lines(INPUT_FILE)
    maze = [x.strip() for x in lines]
    y = 0
    for r in maze:
        if r[0] == ';':
            continue
        x = 0
        for c in r:
            if c != "#":
                graph[(x, y)] = []
                if c != '.':
                    deps[c] = (x, y)
            x += 1
        y += 1
    for p in graph.keys():
        for d in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
            test = (p[0] + d[0], p[1] + d[1])
            if test in graph.keys() and test not in graph[p]:
                graph[p].append(test)

    d = {}
    for k, v in deps.items():
        d[k] = findAdjacent(graph, deps, v)

    graph = d
    total_keys = sum(node.islower() for node in d)
    min_steps = minSteps('@', total_keys)
    return min_steps


def solve_part2():
    global graph
    minSteps.cache_clear()
    reachableKeys.cache_clear()

    graph = defaultdict(list)
    deps = {}

    lines = AoCInput.read_lines(INPUT_FILE2)
    maze = [x.strip() for x in lines]
    robot = 1
    y = 0
    for r in maze:
        if r[0] == ';':
            continue
        x = 0
        for c in r:
            if c != "#":
                graph[(x, y)] = []
                if c != '.':
                    if c == '@':
                        deps[str(robot)] = (x, y)
                        robot += 1
                    else:
                        deps[c] = (x, y)
            x += 1
        y += 1
    for p in graph.keys():
        for d in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
            test = (p[0] + d[0], p[1] + d[1])
            if test in graph.keys() and test not in graph[p]:
                graph[p].append(test)

    d = {}
    for k, v in deps.items():
        d[k] = findAdjacent(graph, deps, v)

    graph = d
    total_keys = sum(node.islower() for node in d)
    min_steps = minSteps('1234', total_keys)
    return min_steps


answer1 = solve_part1()
AoCUtils.print_solution(1, f"The minimum steps to get all keys is {answer1}")

answer2 = solve_part2()
AoCUtils.print_solution(2, f"The minimum steps to get all keys is {answer2}")
