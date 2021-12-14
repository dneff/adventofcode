
from collections import defaultdict

def printSolution(x):
    print(f"The solution is {x}")


def processPolymer(polymer, elements, rules):
    result = defaultdict(int)
    for k in polymer.keys():
        elements[rules[k]] += polymer[k]
        left, right = k[0] + rules[k], rules[k] + k[1]
        result[left] += polymer[k]
        result[right] += polymer[k]

    return result, elements


def main():
    test = 'test.txt'
    puzzle = 'input.txt'
    
    file = open(puzzle, 'r')
    polymer_string = file.readline().strip()
    file.readline()

    insertions = {}
    for line in file.readlines():
        k, v = line.strip().split(' -> ')
        insertions[k[0] + k[1]] = v

    polymer = defaultdict(int)
    elements = defaultdict(int)

    for i in range(len(polymer_string) - 1):
        polymer[polymer_string[i:i+2]] += 1

    for p in polymer_string:
        elements[p] += 1

    cycles = 40
    for cycle in range(cycles):
        polymer, elements = processPolymer(polymer, elements, insertions)
    
    printSolution(max(elements.values()) - min(elements.values()))


if __name__ == "__main__":
    main()
