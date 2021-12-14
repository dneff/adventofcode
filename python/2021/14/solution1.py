
from collections import defaultdict

def printSolution(x):
    print(f"The solution is {x}")


def processPolymer(polymer, rules):
    result = ''
    for i in range(len(polymer) - 1):
        current, next = polymer[i], polymer[i+1]
        result += current + rules[(current, next)]
    result += polymer[-1]
    return result


def main():
    test = 'test.txt'
    puzzle = 'input.txt'
    
    file = open(puzzle, 'r')
    polymer = file.readline().strip()
    file.readline()
    
    insertions = {}
    for line in file.readlines():
        k, v = line.strip().split(' -> ')
        insertions[(k[0], k[1])] = v

    cycles = 10
    for _ in range(cycles):
        polymer = processPolymer(polymer, insertions)
    
    counts = defaultdict(int)
    for p in polymer:
        counts[p] += 1

    printSolution(max(counts.values()) - min(counts.values()))


if __name__ == "__main__":
    main()
