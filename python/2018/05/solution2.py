from collections import deque
from string import ascii_uppercase

def printSolution(x):
    print(f"The solution is {x}")

def willReact(x, y):
    return (x.lower() == y.lower() and ((x.islower() and y.isupper()) or (x.isupper() and y.islower())))

def main():
    file = open('input.txt', 'r')
    puzzle = file.readline().strip()
    test = 'dabAcCaCBAcCcaDA'
    polymer = puzzle

    new_polymer = deque()

    eliminated = {}
    for skipped in ascii_uppercase:
        idx = 0
        new_polymer.clear()
        while idx < len(polymer):
            if polymer[idx].upper() == skipped.upper():
                idx += 1
                continue

            if len(new_polymer) == 0:
                new_polymer.appendleft(polymer[idx])
                idx += 1
                continue

            if willReact(polymer[idx], new_polymer[0]):
                new_polymer.popleft()
            else:
                new_polymer.appendleft(polymer[idx])

            idx += 1

        eliminated[skipped] = len(new_polymer)

    shortest_polymer = min(eliminated.values())
    printSolution(shortest_polymer)
    




if __name__ == '__main__':
    main()