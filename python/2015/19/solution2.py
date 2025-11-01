import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, '../../../../aoc-data/2015/19/input')
sys.path.append(os.path.join(SCRIPT_DIR, '../../'))

from aoc_helpers import AoCInput, AoCUtils
import re
from collections import defaultdict


memo = set()


def getPermutations(molecule, transforms):
    global memo

    created = set()
    for element in transforms:
        element_locs = [loc.span() for loc in re.finditer(element, molecule)]
        for loc in element_locs:
            for substitution in transforms[element]:
                possible_molecule = molecule[:loc[0]] + substitution + molecule[loc[1]:]
                if possible_molecule not in memo:
                    created.add(possible_molecule)

    priority_created = [x for x in created if "e" not in x]
    if len(priority_created) > 0:
        return priority_created
    else:
        return list(created)


def dissolveMolecule(start, target, transforms):
    global memo

    if start == target:
        return [target]
    if start in memo:
        return False

    memo.add(start)

    for molecule in getPermutations(start, transforms):
        result = dissolveMolecule(molecule, target, transforms)
        if result:
            result.insert(0, start)
            return result
    return False


def solve_part2():

    replacements = defaultdict(list)
    lines = AoCInput.read_lines(INPUT_FILE)
    for line in lines:
        if not line.strip():
            break
        start, end = line.strip().split(" => ")
        replacements[end].append(start)

    molecule = lines[0].strip()

    result = dissolveMolecule(molecule, 'e', replacements)

    return len(result - 1)

answer = solve_part2()
AoCUtils.print_solution(2, answer)
