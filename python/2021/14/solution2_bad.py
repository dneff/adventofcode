from collections import defaultdict
import copy


def printSolution(x):
    print(f"The solution is {x}")


def processPolymer(polymer, rules):
    start_polymer = polymer
    result = ''
    max_chunk = 0
    while len(polymer) >= 2:
        long_key = max([len(k) for k in rules.keys()])
        chunk_size = min(long_key, len(polymer))
        while polymer[:chunk_size] not in rules.keys():
            chunk_size -= 1

        result += rules[polymer[:chunk_size]][:-1]
        polymer = polymer[chunk_size - 1:]

    if len(polymer) == 1:
        result += polymer
    
    return result


def main():
    test = 'test.txt'
    puzzle = 'input.txt'

    file = open(test, 'r')
    polymer = file.readline().strip()
    file.readline()

    insertions = {}
    for line in file.readlines():
        k, v = line.strip().split(' -> ')
        insertions[k] = k[0] + v + k[1]

    cycles = 40
    for cycle in range(cycles):
        print(f"cycle: {cycle}")

        updated = copy.copy(insertions)
        for v in insertions.values():
            if len(v) <= cycle + 2:
                updated[v] = processPolymer(v, insertions)
        insertions = updated

        polymer = processPolymer(polymer, insertions)
    counts = defaultdict(int)
    for p in polymer:
        counts[p] += 1

    printSolution(max(counts.values()) - min(counts.values()))


if __name__ == "__main__":
    main()
