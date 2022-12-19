
from collections import defaultdict, deque

def printSolution(x):
    print(f"The solution is {x}")


class Node():
    def __init__(self):
        self.children = ['',]
        self.metadata = []
    
    def getValue(self):
        value = 0
        if len(self.children) == 1:
            value += sum(self.metadata)
        else:
            for child in self.metadata:
                if child == 0:
                    continue
                else:
                    try:
                        value += self.children[child].getValue()
                    except IndexError:
                        pass
        return value

def getNode(input):
    root = Node()
    subnodes, metadata = input.pop(0), input.pop(0)

    for node in range(subnodes):
        root.children.append(getNode(input))
        
    for value in range(metadata):
        root.metadata.append(input.pop(0))
    return root


def main():
    puzzle = 'input.txt'
    test = 'test.txt'
    active = puzzle

    file = open(active, 'r')
    input = [int(x) for x in file.readline().strip().split()]

    tree = getNode(input)

    printSolution(tree.getValue())




if __name__ == "__main__":
    main()