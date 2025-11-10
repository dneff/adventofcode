import os
import sys

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils  # noqa: E402

# Input file path
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2019/6/input')


def objectDistance(graph, src, dest):
    objects = [src]
    if graph[src] == dest:
        objects.append(dest)
    else:
        objects.extend(objectDistance(graph, graph[src], dest))
    return objects


def solve_part1():
    lines = AoCInput.read_lines(INPUT_FILE)
    graph = {}
    for line in lines:
        pair = line.strip().split(')')
        graph[pair[1]] = pair[0]

    orbits = 0
    for k in graph.keys():
        orbits += len(objectDistance(graph, k, 'COM')) - 1
    return orbits


def solve_part2():
    lines = AoCInput.read_lines(INPUT_FILE)
    graph = {}
    for line in lines:
        pair = line.strip().split(')')
        graph[pair[1]] = pair[0]

    you_path = objectDistance(graph, 'YOU', 'COM')
    santa_path = objectDistance(graph, 'SAN', 'COM')

    while you_path[-2] == santa_path[-2]:
        you_path.pop()
        santa_path.pop()

    # transfers equals path lengths minus YOU minus SAN minus two as we're counting edges, not nodes
    return len(you_path) + len(santa_path) - 4


answer1 = solve_part1()
AoCUtils.print_solution(1, answer1)

answer2 = solve_part2()
AoCUtils.print_solution(2, answer2)