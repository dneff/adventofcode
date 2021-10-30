from collections import deque

def printSolution(x):
    print(f"The solution is {x}")

def willReact(x, y):
    if x.lower() != y.lower():
        return False
    if (x.islower() and y.isupper()):
        return True
    if (x.isupper() and y.islower()):
        return True
    return False

def main():
    file = open('input.txt', 'r')
    puzzle = file.readline().strip()
    test = 'dabAcCaCBAcCcaDA'
    polymer = puzzle

    new_polymer = deque()

    idx = 0

    while idx < len(polymer):
        if len(new_polymer) == 0:
            new_polymer.appendleft(polymer[idx])
            idx += 1
            continue

        if polymer[idx].upper() == new_polymer[0].upper():
            if willReact(polymer[idx], new_polymer[0]):
                new_polymer.popleft()
            else:
                new_polymer.appendleft(polymer[idx])
        else:
            new_polymer.appendleft(polymer[idx])

        idx += 1

    printSolution(len(new_polymer))
    




if __name__ == '__main__':
    main()