
from collections import defaultdict, deque

def printSolution(x):
    print(f"The solution is {x}")

def getMetadataSum(input):
    print(len(input))
    sum = 0
    subnodes, metadata = input.pop(0), input.pop(0)
    for node in range(subnodes):
        sum += getMetadataSum(input)
    for value in range(metadata):
        sum += input.pop(0)
    return sum


def main():
    puzzle = 'input.txt'
    test = 'test.txt'
    active = puzzle

    file = open(active, 'r')
    input = [int(x) for x in file.readline().strip().split()]

    printSolution(getMetadataSum(input))



if __name__ == "__main__":
    main()